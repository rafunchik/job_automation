import openai
import os

# Replace with your actual OpenAI API key
OPENAI_KEY = os.environ['OPENAI_KEY']


def is_remote(job_description: str) -> str:
    # Your GPT-3 prompt
    prompt = f"""
        Please analyze the following job description <<{job_description}>> and classify as either "Remote," "Hybrid," or 
        "On-site." See some examples below: 
        
        **Remote Job Descriptions:**
        
        1. Job Title: Remote Software Developer
           Description: We are looking for an experienced software developer to join our team. This is a fully remote position, 
           and you can work from anywhere with a stable internet connection.
        
        2. Job Title: Virtual Customer Support Representative
           Description: Join our customer support team and provide assistance to our clients. This is a 100% remote position, 
           and you'll communicate with customers via phone and email.
        
        **Hybrid Job Descriptions:**
        
        3. Job Title: Marketing Manager
           Description: We are seeking a Marketing Manager to lead our marketing efforts. While the role offers flexibility, 
           you'll be expected to spend a portion of your week at our office for team meetings and collaboration.
        
        4. Job Title: Sales Associate
           Description: As a Sales Associate, you'll work both remotely and in our downtown office. You'll have the option to 
           choose your work arrangement, with a blend of in-office and remote work.
            
        Please classify the job description as Remote, Hybrid, or On-site based on the provided description. If the description doesn't 
        provide enough information, please classify as Unknown.
        """
    # Make a request to the OpenAI API
    response = openai.Completion.create(
        engine="text-davinci-002",  #"gpt-3.5-turbo",  #"text-davinci-002",  # You can use another engine if preferred
        prompt=prompt,
        max_tokens=50,  # Adjust the max_tokens as needed to control response length
        api_key=OPENAI_KEY
    )
    # Extract the generated response
    job_classification = response.choices[0].text.strip()
    # Print the result
    return job_classification


def is_remote2(job_description: str) -> str:
    question = "As system answer, ss this a remote or a hybrid role? If the description doesn't provide enough information just say Unknown."
    # Your chat-like conversation
    conversation = [
        {"role": "user", "content": f"""Description: We are looking for an experienced software developer to join our 
           team. This is a fully remote position, and you can work from anywhere with a stable internet connection. 
           {question}"""},
        {"role": "system", "content": "Remote."},
        {"role": "user", "content": f"""Description: We are seeking a Marketing Manager to lead our marketing efforts. 
           While the role offers flexibility, you'll be expected to spend a portion of your week at our office for team 
           meetings and collaboration. {question}"""},
        {"role": "system", "content": "Hybrid."},
        {"role": "user", "content": f"""Description: Join our customer support team and provide assistance to our clients.
           This is a 100% remote position, and you'll communicate with customers via phone and email. {question}"""},
        {"role": "system", "content": "Remote."},
        {"role": "user", "content": f"""Description: As a Sales Associate, you'll work both remotely and in our downtown 
           office. You'll have the option to choose your work arrangement, with a blend of in-office and remote work. 
           {question}"""},
        {"role": "system", "content": "Hybrid."},
        {"role": "user", "content": f"""{question} <<Description: {job_description}>> """},

    ]
    return _ask_chatgpt(conversation)


def is_contract(job_description: str) -> str:
    question = "As system answer, is this a contract or a permanent role? If the description doesn't provide enough information just say Unknown."

    # Your chat-like conversation
    conversation = [
        {"role": "user", "content": """I would like to know whether an advertised job is a contract or a permanent role, 
        will provide some rules and examples"""},
        {"role": "user", "content": "If the description mentions a salary and it is more than 50k 0r 50000 the role is a permanent role."},
        {"role": "user", "content": "If the description mentions a salary and it is less than a 1000 the role is a contract role."},
        {"role": "user", "content": "If the description mentions a bonus or other benefits it is a permanent role."},
        {"role": "user", "content": f"""Description: We are seeking a web developer to work on a short-term project. The 
           contract duration is 6 months, with the possibility of extension based on performance. {question}"""},
        {"role": "system", "content": "Contract."},
        {"role": "user", "content": f"""Description: The roles will be offered as part of industrial placements to be 
        undertaken during the 2024/2025 academic year. We are looking for an Analyst Data Engineer and Analyst Data 
        Scientist who will join a growing team who deliver data science and analytical capabilities on our 100% Azure 
        cloud-based infrastructure. We are a people first company and your growth and development is an important part 
        of our view of success. BenefitsAbout what we offer Placement duration to be agreed with contract (between 9 – 12 months)
        Placement start date to be agreed (between June & September) Competitive salary between £17,000 - £23,000 per annum 
        / pro rata‘Fresh Air Fridays’ - the flexible option to finish early on a Friday where possible. , Salary: 17000 - 23000 {question}"""},
        {"role": "system", "content": "Permanent."},
        {"role": "user", "content": f"""Description: We are looking for a Senior Software Engineer to join our growing 
        team. This is a full-time position, with 25 days of vacation and with opportunities for career advancement. {question}"""},
        {"role": "system", "content": "Permanent."},
        {"role": "user", "content": f"""Description: Join our design team on a contract basis to assist with a specific 
        project. The contract will last for 12 months, with potential for additional assignments. {question}"""},
        {"role": "system", "content": "Contract."},
        {"role": "user", "content": f"""Description: Contract AWS Data Engineer, {question}"""},
        {"role": "system", "content": "Contract."},
        {"role": "user", "content": f"""Description: Join our company as an HR Manager. This is a permanent role 
        responsible for overseeing our human resources department and ensuring HR operations run smoothly. {question}"""},
        {"role": "system", "content": "Permanent."},
        {"role": "user", "content": f"""Description: Join our company as an HR Manager. This company has a great work 
        ethos which offers a modern hybrid working model, fantastic benefits which invest in your health and wellbeing, 
        bonus and a generous salary. {question}"""},
        {"role": "system", "content": "Permanent."},
        {"role": "user", "content": f"""Description: Join our design team! Fast growing company offering a great salary, 
        fantastic benefits and bonus. {question}"""},
        {"role": "system", "content": "Permanent."},
        {"role": "user", "content": f"""Description: , Salary 225000 - 300000  k {question}"""},
        {"role": "system", "content": "Permanent."},
        {"role": "user", "content": f"""{question} <<Description: {job_description}>> """},
    ]
    return _ask_chatgpt(conversation)


def _ask_chatgpt(messages: list) -> str:

    # Make a request to the OpenAI API using the chat/completions endpoint
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",  # Use the chat model
        messages=messages,  # Provide the conversation as messages
        max_tokens=50,
        api_key=OPENAI_KEY
    )

    # Extract the assistant's reply
    assistant_reply = response['choices'][0]['message']['content']
    print(assistant_reply)
    return assistant_reply
