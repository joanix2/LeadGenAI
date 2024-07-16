from application import app

@app.route('/upload_image', methods=['POST'])
def upload_image():
    title = request.form.get('title')
    image_file = request.files.get('image')

    if not title or not image_file:
        return jsonify({'error': 'Title and image file are required'}), 400

    # Save the image to GridFS
    image_id = fs.put(image_file, filename=image_file.filename)

    # Save the image metadata to the Image collection
    image = Image(title=title, image_id=str(image_id))
    image.save()

    return jsonify(image.to_json()), 201

@app.route('/get_image/<image_id>', methods=['GET'])
def get_image(image_id):
    try:
        image_file = fs.get(ObjectId(image_id))
        return send_file(BytesIO(image_file.read()), mimetype=image_file.content_type)
    except Exception as e:
        return jsonify({'error': str(e)}), 404


@app.route('/add_funnel', methods=['POST'])
def add_funnel():
    data = request.json
    
    # Extract and validate the necessary fields
    route_name = data.get('route_name')
    landing_page_data = data.get('landing_page')
    form_page_data = data.get('form_page')
    
    if not route_name or not landing_page_data or not form_page_data:
        return jsonify({'error': 'Missing required fields'}), 400

    # Create or retrieve the LandingPage
    landing_page = LandingPage(**landing_page_data)
    landing_page.save()

    # Create or retrieve the Form and its Questions/Answers
    questions = []
    for question_data in form_page_data.get('questions', []):
        answers = []
        for answer_data in question_data.get('answers', []):
            answer = Answer(**answer_data)
            answer.save()
            answers.append(answer)
        question = Question(text=question_data['text'], answers=answers, multiple_choice=question_data.get('multiple_choice', False))
        question.save()
        questions.append(question)
    
    form = Form(title=form_page_data['title'], questions=questions)
    form.save()

    # Create the Funnel
    funnel = Funnel(route_name=route_name, landing_page=landing_page, form_page=form)
    funnel.save()

    return jsonify(funnel.to_json()), 201

@app.route('/create_form', methods=['POST'])
def create_form():
    title = request.form.get('title')

    form = Form(title=title)
    form.save()

    return jsonify(form.to_json()), 201

@app.route('/add_question/<form_id>', methods=['POST'])
def add_question(form_id):
    text = request.form.get('text')
    multiple_choice = request.form.get('multiple_choice', 'false').lower() == 'true'

    question = Question(text=text, multiple_choice=multiple_choice)
    question.save()

    form = Form.objects(id=form_id).first()
    if not form:
        return jsonify({'error': 'Form not found'}), 404

    form.questions.append(question)
    form.save()

    return jsonify(question.to_json()), 201

@app.route('/add_answer/<question_id>', methods=['POST'])
def add_answer(question_id):
    text = request.form.get('text')
    is_correct = request.form.get('is_correct', 'false').lower() == 'true'

    answer = Answer(text=text, is_correct=is_correct)
    answer.save()

    question = Question.objects(id=question_id).first()
    if not question:
        return jsonify({'error': 'Question not found'}), 404

    question.answers.append(answer)
    question.save()

    return jsonify(answer.to_json()), 201

@app.route('/create_landing_page', methods=['POST'])
def create_landing_page():
    title = request.form.get('title')
    text = request.form.get('text')
    image = request.form.get('image')

    landing_page = LandingPage(title=title, text=text, image=image)
    landing_page.save()

    return jsonify(landing_page.to_json()), 201

@app.route('/create_funnel', methods=['POST'])
def create_funnel():
    landing_page_ids = request.form.getlist('landing_page_ids')
    landing_pages = [LandingPage.objects(id=id).first() for id in landing_page_ids]

    funnel = Funnel(landing_pages=landing_pages)
    funnel.save()

    return jsonify(funnel.to_json()), 201

@app.route('/create_user', methods=['POST'])
def create_user():
    username = request.form.get('username')
    email = request.form.get('email')

    user = User(username=username, email=email)
    user.save()

    return jsonify(user.to_json()), 201

@app.route('/add_response/<user_id>', methods=['POST'])
def add_response(user_id):
    answer_id = request.form.get('answer_id')
    answer = Answer.objects(id=answer_id).first()

    if not answer:
        return jsonify({'error': 'Answer not found'}), 404

    user = User.objects(id=user_id).first()
    if not user:
        return jsonify({'error': 'User not found'}), 404

    user.responses.append(answer)
    user.save()

    return jsonify(user.to_json()), 201
    
@app.route('/get_form/<form_id>', methods=['GET'])
def get_form(form_id):
    form = Form.objects(id=form_id).first()
    if not form:
        return jsonify({'error': 'Form not found'}), 404

    return jsonify(form.to_json()), 200
    
    
@app.route('/get_landing_page/<landing_page_id>', methods=['GET'])
def get_landing_page(landing_page_id):
    landing_page = LandingPage.objects(id=landing_page_id).first()
    if not landing_page:
        return jsonify({'error': 'LandingPage not found'}), 404

    return jsonify(landing_page.to_json()), 200


