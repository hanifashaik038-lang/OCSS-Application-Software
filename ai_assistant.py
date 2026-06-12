import openai
import os
from dotenv import load_dotenv
import json

load_dotenv()

class AIAssistant:
    def __init__(self):
        self.api_key = os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError("OPENAI_API_KEY not set in environment")
        openai.api_key = self.api_key
    
    def summarize_text(self, text, summary_type="short"):
        """Summarize text using AI"""
        try:
            if summary_type == "short":
                prompt = f"""Provide a concise summary of the following text in 5-7 key points:

{text}

Format the response as bullet points."""
            else:
                prompt = f"""Provide a detailed summary of the following text with explanations:

{text}

Include main concepts, key details, and important takeaways."""
            
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are an expert study assistant helping students learn. Be clear and concise."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=1500
            )
            
            return response.choices[0].message.content
        except Exception as e:
            return f"Error generating summary: {str(e)}"
    
    def explain_concept(self, concept, material_text):
        """Explain a difficult concept in simple language"""
        try:
            prompt = f"""A student wants to understand '{concept}' from their study material.

Study Material:
{material_text}

Please explain '{concept}' in very simple language:
1. Use everyday analogies
2. Break it into small parts
3. Give examples
4. Highlight key points
5. Point out common mistakes to avoid"""
            
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are an expert educator who explains complex concepts in simple, engaging language that students understand."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=2000
            )
            
            return response.choices[0].message.content
        except Exception as e:
            return f"Error explaining concept: {str(e)}"
    
    def generate_flashcards(self, text, num_cards=10):
        """Generate flashcards from text"""
        try:
            prompt = f"""Create exactly {num_cards} study flashcards from this material.

Material:
{text}

For each flashcard, create:
- A clear question on one side
- A concise answer on the other side

Return the response ONLY as a JSON array with this exact format:
[
  {{"question": "What is...", "answer": "..."}},
  {{"question": "How does...", "answer": "..."}},
  ...
]

Only return the JSON array, no other text."""
            
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are an expert at creating effective study flashcards. Always return valid JSON."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=3000
            )
            
            response_text = response.choices[0].message.content
            # Try to parse JSON
            try:
                flashcards = json.loads(response_text)
                return flashcards
            except:
                # If JSON parsing fails, return error with raw response
                return {"error": "Could not parse response", "raw": response_text}
        except Exception as e:
            return {"error": str(e)}
    
    def generate_revision_notes(self, text):
        """Generate comprehensive revision notes"""
        try:
            prompt = f"""Create detailed revision notes from this study material.

Material:
{text}

Organize the notes with these sections:
1. **Key Definitions** - Important terms and their meanings
2. **Important Concepts** - Main ideas and explanations
3. **Key Formulas/Points** - Critical formulas or bullet points
4. **Examples** - Real-world applications
5. **Common Mistakes** - Mistakes students often make
6. **Quick Tips** - Memory aids and shortcuts
7. **Practice Questions** - Questions to test understanding"""
            
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are an expert at creating comprehensive revision notes for students."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=3000
            )
            
            return response.choices[0].message.content
        except Exception as e:
            return f"Error generating revision notes: {str(e)}"
    
    def answer_question(self, question, context_text):
        """Answer specific questions based on provided material"""
        try:
            prompt = f"""Based ONLY on the following study material, answer this question:

Study Material:
{context_text}

Student Question: {question}

Instructions:
1. Answer ONLY based on the material provided
2. If the answer is not in the material, say so clearly
3. Explain step-by-step if needed
4. Provide examples from the material"""
            
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a helpful study assistant. Answer only based on provided material."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=2000
            )
            
            return response.choices[0].message.content
        except Exception as e:
            return f"Error answering question: {str(e)}"
    
    def generate_mcq_questions(self, text, num_questions=10, difficulty="Medium"):
        """Generate MCQ questions from text"""
        try:
            prompt = f"""Create exactly {num_questions} multiple choice questions ({difficulty} difficulty) from this material.

Material:
{text}

For each question, provide:
- The question
- Exactly 4 options (A, B, C, D)
- The correct answer
- Brief explanation of why it's correct

Return ONLY as JSON array in this format:
[
  {{
    "question": "Question text?",
    "options": {{"A": "option", "B": "option", "C": "option", "D": "option"}},
    "correct_answer": "A",
    "explanation": "Why A is correct"
  }}
]"""
            
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are an expert exam question creator. Always return valid JSON."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=4000
            )
            
            response_text = response.choices[0].message.content
            try:
                questions = json.loads(response_text)
                return questions
            except:
                return {"error": "Could not parse questions", "raw": response_text}
        except Exception as e:
            return {"error": str(e)}
    
    def generate_short_answer_questions(self, text, num_questions=5):
        """Generate short answer questions"""
        try:
            prompt = f"""Create exactly {num_questions} short-answer study questions from this material.

Material:
{text}

For each question, provide:
- The question
- A model answer (3-5 lines)
- Key points to include

Return ONLY as JSON:
[
  {{
    "question": "Question?",
    "model_answer": "Sample answer",
    "key_points": ["point1", "point2"]
  }}
]"""
            
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are an expert at creating short-answer questions."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=2000
            )
            
            response_text = response.choices[0].message.content
            try:
                questions = json.loads(response_text)
                return questions
            except:
                return {"error": "Could not parse", "raw": response_text}
        except Exception as e:
            return {"error": str(e)}
    
    def generate_long_answer_questions(self, text, num_questions=3):
        """Generate long-answer/essay questions"""
        try:
            prompt = f"""Create exactly {num_questions} long-answer/essay questions from this material.

Material:
{text}

For each question, provide:
- The question (complex, requiring detailed answer)
- Expected answer structure (outline with points to cover)
- Marking breakdown

Return ONLY as JSON:
[
  {{
    "question": "Long question?",
    "answer_structure": ["Point 1", "Point 2", "Point 3"],
    "marks": 10
  }}
]"""
            
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are expert at creating thought-provoking long-answer questions."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=2000
            )
            
            response_text = response.choices[0].message.content
            try:
                questions = json.loads(response_text)
                return questions
            except:
                return {"error": "Could not parse", "raw": response_text}
        except Exception as e:
            return {"error": str(e)}
