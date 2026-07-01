# import argparse
# import os
# from dotenv import load_dotenv
# from google import genai
# from google.genai import types
#
# from call_function import (
#     call_function,
# )
# from functions.get_file_content import schema_get_file_content
# from functions.get_files_info import schema_get_files_info
# from functions.run_python_file import schema_run_python_file
# from functions.write_file import schema_write_file
# from prompts import system_prompt
#
#
# # =========================
# # CLIENT SETUP
# # =========================
# def config_client():
#     load_dotenv()
#
#     api_key = os.environ.get("GEMINI_API_KEY")
#     if not api_key:
#         raise RuntimeError("GEMINI_API_KEY not found.")
#
#     return genai.Client(api_key=api_key)
#
#
# # =========================
# # MODEL CALL
# # =========================
# def generate_content(client, messages):
#     return client.models.generate_content(
#         model="gemini-2.5-pro",        contents=messages,
#         config={
#             "system_instruction": system_prompt,
#             "tools": [
#                 {
#                     "function_declarations": [
#                         schema_get_files_info,
#                         schema_get_file_content,
#                         schema_run_python_file,
#                         schema_write_file,
#                     ]
#                 }
#             ],
#             "temperature": 0
#         }
#     )
#
#
# # =========================
# # MAIN AGENT LOOP
# # =========================
# def main():
#     parser = argparse.ArgumentParser(description="Chatbot CLI")
#     parser.add_argument("user_prompt", type=str)
#     parser.add_argument("--verbose", action="store_true")
#     args = parser.parse_args()
#
#     client = config_client()
#
#     # 🧠 memory
#     messages = [
#         types.Content(
#             role="user",
#             parts=[types.Part(text=args.user_prompt)]
#         )
#     ]
#
#     # 🔁 AGENT LOOP
#     for _ in range(20):
#
#         response = generate_content(client, messages)
#
#         candidate = response.candidates[0]
#         parts = candidate.content.parts
#
#         function_calls = [
#             p.function_call for p in parts if getattr(p, "function_call", None)
#         ]
#
#         # ======================
#         # TOOL CALLS FIRST
#         # ======================
#         if function_calls:
#
#             print(f" - Calling function(s): {[fc.name for fc in function_calls]}")
#
#             tool_results = []
#
#             for fc in function_calls:
#                 result = call_function(fc, verbose=args.verbose)
#
#                 if result.parts:
#                     tool_results.extend(result.parts)
#
#             # مهم: نضيف نتائج الأدوات فقط
#             messages.append(
#                 types.Content(
#                     role="user",
#                     parts=tool_results
#                 )
#             )
#
#             continue
#
#         # ======================
#         # FINAL ANSWER
#         # ======================
#         final_text = candidate.content.parts[0].text
#
#         if final_text:
#             print(final_text)
#             return
#
#     # safety stop
#     print("❌ Max iterations reached")
#     exit(1)


import argparse
import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types

from call_function import (
    call_function,
)
from functions.get_file_content import schema_get_file_content
from functions.get_files_info import schema_get_files_info
from functions.run_python_file import schema_run_python_file
from functions.write_file import schema_write_file
from prompts import system_prompt


# =========================
# CLIENT SETUP
# =========================
def config_client():
    load_dotenv()

    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        raise RuntimeError("GEMINI_API_KEY not found.")

    return genai.Client(api_key=api_key)


# =========================
# MODEL CALL
# =========================
def generate_content(client, messages):
    return client.models.generate_content(
        model="gemini-2.5-pro",
        contents=messages,
        config={
            "system_instruction": system_prompt,
            "tools": [
                {
                    "function_declarations": [
                        schema_get_files_info,
                        schema_get_file_content,
                        schema_run_python_file,
                        schema_write_file,
                    ]
                }
            ],
            "temperature": 0
        }
    )


# =========================
# MAIN AGENT LOOP
# =========================
def main():
    parser = argparse.ArgumentParser(description="Chatbot CLI")
    parser.add_argument("user_prompt", type=str)
    parser.add_argument("--verbose", action="store_true")
    args = parser.parse_args()

    client = config_client()

    # 🧠 memory
    messages = [
        types.Content(
            role="user",
            parts=[types.Part.from_text(text=args.user_prompt)]
        )
    ]

    # 🔁 AGENT LOOP
    for _ in range(20):

        response = generate_content(client, messages)

        # التحقق من وجود candidates (كما طلب التكليف في بداية الحلقة)
        if not response.candidates:
            print("Error: No candidates returned from the model.")
            sys.exit(1)

        candidate = response.candidates[0]

        # 1. الإضافة الأولى: إضافة رد النموذج (الذي قد يحتوي على طلبات أدوات أو النص النهائي)
        if candidate.content:
            messages.append(candidate.content)

        parts = candidate.content.parts

        # البحث عن أي طلبات لاستدعاء الدوال
        function_calls = [
            p.function_call for p in parts if getattr(p, "function_call", None)
        ]

        # ======================
        # TOOL CALLS FIRST
        # ======================
        if function_calls:
            tool_results = []

            for fc in function_calls:
                # ملاحظة: دالة call_function تطبع اسم الأداة تلقائياً
                result_content = call_function(fc, verbose=args.verbose)

                if result_content.parts:
                    tool_results.extend(result_content.parts)

            # 2. الإضافة الثانية: إضافة نتائج الأدوات إلى المحادثة
            if tool_results:
                messages.append(
                    types.Content(
                        role="user",
                        parts=tool_results
                    )
                )

            # الاستمرار في الحلقة (Feedback loop) ليرى النموذج النتيجة ويقرر الخطوة التالية
            continue

        # ======================
        # FINAL ANSWER
        # ======================
        # إذا لم يكن هناك أي Function calls، فهذا يعني أن النموذج أصدر الإجابة النهائية
        final_text = parts[0].text if parts else ""

        if final_text:
            print("Final response:")
            print(final_text)
            return

    # في حال تجاوز عدد المحاولات 20 مرة دون الوصول لإجابة نهائية
    print("Error: The agent reached the maximum number of iterations (20) without a final response.")
    sys.exit(1)


if __name__ == "__main__":
    main()