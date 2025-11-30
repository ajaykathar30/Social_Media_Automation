# from google.generativeai import GenerativeModel, Client
# from PIL import Image

# # 🔹 Add your API key here
# client = genai.Client(api_key="AIzaSyABgAcbB07pYwyOk4kOaPxuLaxM0bdl5no")

# prompt = (
#     "Create a high-quality Instagram post graphic for students announcing exam results. "
#     "Main headline text on the image: IBPS PO Mains Result 2025 — Coming Soon. "
#     "Sub-text: IBPS PO Mains Result to be announced on ibps.in; Exam held on October 12, 2025; "
#     "Check your results & download scorecard using Application No. + Password. "
#     "Visual style: Elegant, modern, and highly attractive design for competitive exam students. "
#     "Use professional colors (blue, navy, and white), banking/education theme, and include elements "
#     "like a result notification graphic, calendar icons, and a laptop with the IBPS website on screen. "
#     "Add a positive motivational tone. Audience: Students preparing for banking exams in India. "
#     "Aspect ratio: 4:5 Instagram post. Do not add watermarks or logos."
# )

# response = client.models.generate_content(
#     model="gemini-2.5-flash-image",
#     contents=[prompt],
# )

# for part in response.parts:
#     if hasattr(part, "text") and part.text is not None:
#         print(part.text)
#     elif hasattr(part, "inline_data") and part.inline_data is not None:
#         image = part.as_image()
#         image.save("generated_image.png")

# print("Image saved as generated_image.png")


from google import genai
from google.genai import types
from PIL import Image

client = genai.Client(api_key="AIzaSyABgAcbB07pYwyOk4kOaPxuLaxM0bdl5no")

# prompt = (
#     "Generate an image on instagram post . Create a high-quality Instagram post graphic for students announcing exam results. "
#     "Main headline text on the image: IBPS PO Mains Result 2025 — Coming Soon. "
#     "Sub-text: IBPS PO Mains Result to be announced on ibps.in; Exam held on October 12, 2025; "
#     "Check your results & download scorecard using Application No. + Password. "
#     "Visual style: Elegant, modern, and highly attractive design for competitive exam students. "
#     "Use professional colors (blue, navy, and white), banking/education theme, and include elements "
#     "like a result notification graphic, calendar icons, and a laptop with the IBPS website on screen. "
#     "Add a positive motivational tone. Audience: Students preparing for banking exams in India. "
#     "Aspect ratio: 4:5 Instagram post. Do not add watermarks or logos."
# )
prompt=("generate image of a cat playing with ball")

response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents=[prompt],
)

for part in response.parts:
    if part.text is not None:
        print(part.text)
    elif part.inline_data is not None:
        image = part.as_image()
        image.save("generated_image.png")