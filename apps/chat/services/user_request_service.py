from apps.chat.models.chat_history import UserOpenAIChatHistory, UserOpenAIChatHistoryQuestion
from apps.main.models.languages import Language
from apps.main.models.project_category import ProjectCategory
from apps.main.models.question_group import QuestionGroup
from apps.main.models.question import Question, QuestionOption
from rest_framework.exceptions import ValidationError
from apps.openapi.open_api_client import OpenAIHelper
from apps.chat.models.user_chat import UserChat
from apps.chat.utils import replace_boolean_tokens
import tiktoken


class UserRequestService:
    
    @staticmethod
    def build_response(user, data, chat):
        project_id = data.get('project_id')
        language_id = data.get('language_id')
        project = UserRequestService.get_object(project_id , ProjectCategory , model_name = "Project group")
        prompts = []
        if language_id:
            language = Language.objects.get(id=language_id)
        else:    
            language = user.language if user.language else Language.objects.filter(code='uz').first()
        if not language:
            raise ValidationError(f"User language not found")  
        if not chat:
            chat = UserRequestService.create_chat_for_user(user, project) 
        project_name = project.translations.filter(language=language).first()
        if not project_name:
            raise ValidationError(f"Project name not found")
        project_name = project_name.name        
        project_prompt = project.prompts.filter(language=language).first()
        if not project_prompt: 
            raise ValidationError(f"Project prompt not found")
        project_prompt = project_prompt.prompt        
        
        final_prompt = f"Направление: {project_name} " 
        question_groups = []
        chat_history_question = []
        for question in data.get('questions', []):
            chat_history_question.append(question)
            question_group_id = question.get('question_group')
            question_id = question.get('question_id')
            boolean = question.get('boolean_answer')
            question_group = UserRequestService.get_object(question_group_id , QuestionGroup , model_name = "Question group")
            db_question = UserRequestService.get_object(question_id , Question , model_name = "Question")
            options = question.get('options', [])
            free_answer = question.get('free_answer', '')
            question_group_name = question_group.translations.filter(language=language).first().name 
            if question_group_name not in question_groups:
                question_groups.append(question_group_name)
                prompts = f"{question_group_name}:  "
            else:    
                prompts = f" "
            prompts = UserRequestService.generate_prompt(prompts, db_question, language, options, boolean, free_answer)
            final_prompt += prompts + " "
        print()    
        print("final prompt ", final_prompt)    
        print()    
        encoding = tiktoken.encoding_for_model("gpt-4o")
        # tokenlar sonini hisoblash
        num_tokens = len(encoding.encode(final_prompt))
        if user.is_active_user and user.total_tokens > 0 :
            if num_tokens + 7 >= user.total_tokens:
                raise ValidationError(detail={
                    "error": True,
                    "message": "User tokens not enough"
                })    
                    
            result = OpenAIHelper.ask_openai(final_prompt, system_prompt=project_prompt)
            prompt_tokens = result["prompt_tokens"]
            completion_tokens = result["completion_tokens"]
            total_tokens = result["total_tokens"]
            cost = OpenAIHelper.calculate_openai_cost(prompt_tokens, completion_tokens, model="gpt-4o")
            result = {
                "result": result["content"],
                "prompt_tokens": prompt_tokens,
                "completion_tokens": completion_tokens,
                "total_tokens": total_tokens,
                "total_cost_usd": cost,
                "chat": {
                    "id": chat.id,
                    "title": chat.title,
                    "created_at": chat.created_at,
                    'message_id':None
                }
            }
            chat_history = UserRequestService.save_chat_history(prompt_text=final_prompt, chat=chat, data=result)
            chat_history_question = UserRequestService.save_chat_history_questions(chat_history, chat_history_question)
            user.total_tokens -= total_tokens
            if user.total_tokens <= 0:
                user.is_active_user = False
            user.save()
            result['chat']['message_id'] = chat_history_question.id
            return result
        else:
            raise ValidationError({
                    "error": True,
                    "message": "User not active"
                })
        
       
    
    @staticmethod
    def save_chat_history_questions(chat_history, questions):
         for question in questions:
            question_group_id = question.get('question_group')
            question_id = question.get('question_id')
            boolean = question.get('boolean_answer')
            question_group = UserRequestService.get_object(question_group_id , QuestionGroup , model_name = "Question group")
            db_question = UserRequestService.get_object(question_id , Question , model_name = "Question")
            options = question.get('options', [])
            chat_history_question = UserOpenAIChatHistoryQuestion.objects.create(
                chat_history=chat_history,
                question_group=question_group,
                question=db_question,
                boolean=boolean
            )
            if options:
                for option_id in options:
                    option = QuestionOption.objects.filter(id=option_id).first()
                    chat_history_question.question_options.add(option)
            return chat_history_question
    @staticmethod
    def get_object(obj_id: int , model, model_name: str):
        obj = model.objects.filter(id=obj_id).first()
        if not obj:
            raise ValidationError(f"Invalid {model_name} id: {obj_id}")
        return obj
    
    @staticmethod
    def create_chat_for_user(user, project):
        chat_count = UserChat.objects.filter(user=user, project=project).count()
        if chat_count > 0:
            chat_count += 1
            chat_count = f"({chat_count})"
        else:
            chat_count = ""
        title = f"{project.translations.filter(language=user.language).first().name} {chat_count}"
        return UserChat.objects.create(user=user, project=project, title=title)
    
    
    

    
    @staticmethod
    def generate_prompt(prompts, question, language: Language , options: list = [], boolean: bool = None, free_answer: str = ""):
        option_str = ""
        if options:
            for option_id in options:
                option = QuestionOption.objects.filter(id=option_id).first()
                option_name = option.translations.filter(language=language).first().value
                option_str += f"{option_name}, "
          
        prompt_name = question.prompts.filter(language=language).first()
        errors = []
        if prompt_name:
            if  question.type == "boolean":
                if boolean in [True, False] :
                    if "{%boolean" in prompt_name.prompt:
                        prompts += replace_boolean_tokens(prompt_name.prompt, boolean)
                else:
                    errors.append("Boolean answer not provided")
            if question.type == "free_answer":    
                if free_answer:
                    prompts += " "+ free_answer
                else:
                    errors.append("Free answer not provided")
            
            if question.type == "select":
                if not option_str:
                    errors.append("Options not provided")
                else:    
                    propmt = prompt_name.prompt.replace("{%options%}", option_str)
                    prompts += f" {propmt}"
        if errors:
            raise ValidationError(errors)        
        
        return prompts


    @staticmethod
    def save_chat_history(prompt_text,  chat, data):
        chat_history = UserOpenAIChatHistory.objects.create(
            chat=chat,
            model_name="gpt-4o",
            prompt_text=prompt_text,
            response_text=data["result"],
            prompt_tokens=data["prompt_tokens"],
            completion_tokens=data["completion_tokens"],
            total_tokens=data["total_tokens"],
            cost_usd=data["total_cost_usd"]
        )
        chat.message_count += 1
        chat.save()    
        return chat_history