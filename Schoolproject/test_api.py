import requests

# Define the API endpoint URL
url = "http://localhost:8000/create-course/"

# Define the JSON data for the course creation
data = {
    "title": "Your Course Title",
    "description": "Your Course Description",
    "price": "123.45",
    "discount": "10.00",
    "is_free": False,
    "class_or_level": "Your Class or Level",
    "course_preview_url": "https://chat.openai.com/c/e56b89bc-cd81-4c36-b6d6-aa24ab52631b",
    "course_category": 1,
    "visibility": True,
    'sections': [
        {
            "section_title": "Section 1",
            "video_lessons": [
                {
                    "title": "Lesson 1",
                    "video_url": "https://example.com/video1.mp4",
                    "summary": "lesson summary"
                },
                {
                    "title": "Lesson 2",
                    "video_url": "https://example.com/video2.mp4",
                    "summary": "lesson summary"
                }
            ],
            "quiz": {
                "title": "Quiz 1",
                "description": "quiz description",
                "questions": [
                    {
                        "question_text": "Question 1",
                        "correct_answer": "aa",
                        "choices": [
                            {
                                "choice_text": "Choice 1",
                                "is_correct": True
                            },
                            {
                                "choice_text": "Choice 2",
                                "is_correct": False
                            }
                        ]
                    },
                    {
                        "question_text": "Question 2",
                        "correct_answer": "aa",
                        "choices": [
                            {
                                "choice_text": "Choice A",
                                "is_correct": True
                            },
                            {
                                "choice_text": "Choice B",
                                "is_correct": False
                            }
                        ]
                    }
                ]
            }
        }
    ]
}


# Define the file path for the cover image
cover_image_path = r'C:/Users/imed\Desktop/Schoolproject/course_covers/1_2gBjfwy.png'

# Create a dictionary of files with the 'cover_image' field
files = {'cover_image': ('cover_image.png', open(cover_image_path, 'rb'))}

# Send a POST request with data and files
response = requests.post(url, data=data, files=files)

# Process the response
print("HTTP Status Code:", response.status_code)
print("Response Content:", response.content)
