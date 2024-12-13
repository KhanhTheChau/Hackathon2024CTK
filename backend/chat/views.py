from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import ValidationError

class SendMessageAPIView(APIView):
    def post(self, request, *args, **kwargs):
        messages = request.data.get("messages", [])

        # Kiểm tra tính hợp lệ của dữ liệu
        if not messages or not isinstance(messages, list):
            raise ValidationError({"error": "Field 'messages' must be a non-empty list."})

        # Lấy tin nhắn mới nhất từ cuối mảng
        latest_message = messages[-1]

        captions = latest_message.get("captions")
        text = latest_message.get("text")

        if text:
            bot_response = self.generate_bot_response(text)
        elif captions:
            bot_response = self.generate_bot_response(captions)
        else:
            raise ValidationError({"error": "Each message must have either 'text' or 'captions'."})

        return Response({
            "message": "successful",
            "answer": bot_response,
            "success": True
        }, status=status.HTTP_200_OK)

    def generate_bot_response(self, content):


        return f"Chưa có câu trả lời, tạm dị đi"
