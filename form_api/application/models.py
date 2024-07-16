from mongoengine import Document, StringField, BooleanField, ListField, ReferenceField

class Image(Document):
    title = StringField(required=True)
    image_id = StringField(required=True)

    def to_json(self):
        return {
            "id": str(self.id),
            "title": self.title,
            "image_id": self.image_id
        }

class Answer(Document):
    text = StringField(required=True)
    
    def to_json(self):
        return {
            "id": str(self.id),
            "text": self.text
        }

class Question(Document):
    text = StringField(required=True)
    answers = ListField(ReferenceField(Answer))
    multiple_choice = BooleanField(default=False)

    def to_json(self):
        return {
            "id": str(self.id),
            "text": self.text,
            "multiple_choice": self.multiple_choice,
            "answers": [answer.to_json() for answer in self.answers]
        }

class Form(Document):
    title = StringField(required=True)
    questions = ListField(ReferenceField(Question))

    def to_json(self):
        return {
            "id": str(self.id),
            "title": self.title,
            "questions": [question.to_json() for question in self.questions]
        }

class LandingPage(Document):
    title = StringField(required=True)
    text = StringField(required=True)
    image = StringField(required=True)  # URL de l'image

    def to_json(self):
        return {
            "id": str(self.id),
            "title": self.title,
            "text": self.text,
            "image": self.image
        }

class Funnel(Document):
    route_name = StringField(required=True)
    landing_page = ReferenceField(LandingPage)
    form_page = ReferenceField(Form)

    def to_json(self):
        return {
            "id": str(self.id),
            "route_name": self.route_name,
            "landing_page": self.landing_page.to_json() if self.landing_page else None,
            "form_page": self.form_page.to_json() if self.form_page else None
        }

class User(Document):
    username = StringField(required=True, unique=True)
    email = StringField(required=True, unique=True)
    
    def to_json(self):
        return {
            "id": str(self.id),
            "username": self.username,
            "email": self.email
        }

class Responses(Document):
    question = ReferenceField(Question)
    answer = ListField(ReferenceField(Answer))
    text = StringField()

    def to_json(self):
        if self.question and self.question.answers:
            return {
                "id": str(self.id),
                "question": self.question.to_json() if self.question else None,
                "answer": [answer.to_json() for answer in self.answer] if self.answer else []
            }
        else:
            return {
                "id": str(self.id),
                "question": self.question.to_json() if self.question else None,
                "text": self.text
            }

class FormResponses(Document):
    user = ReferenceField(User)
    form = ReferenceField(Form)
    responses = ListField(ReferenceField(Responses))

    def to_json(self):
        return {
            "id": str(self.id),
            "user": self.user.to_json() if self.user else None,
            "form": self.form.to_json() if self.form else None,
            "responses": [response.to_json() for response in self.responses]
        }
