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
        images = latest_message.get("images", [])
        sender = latest_message.get("sender")
        text = latest_message.get("text")

        if not sender:
            raise ValidationError({"error": "Field 'sender' is required in each message."})

        # Xử lý logic trả lời bot
        if text:
            bot_response_text = self.generate_bot_response(text)
            response_data = {
                "captions": None,
                "images": [],
                "sender": "Bot",
                "text": bot_response_text
            }
        elif captions and images:
            bot_response_captions = self.generate_bot_response(captions)
            response_data = {
                "captions": bot_response_captions,
                "images": [],
                "sender": "Bot",
                "text": None
            }
        else:
            raise ValidationError({"error": "Each message must have either 'text' or 'captions' with images."})

        return Response(response_data, status=status.HTTP_200_OK)

    def generate_bot_response(self, content):
        """
        Hàm giả lập trả lời từ bot, có thể thay thế bằng logic xử lý thật
        """
        # Hiện tại chỉ trả về phần đầu của nội dung như một phản hồi đơn giản
        return f"Nuôi tôm kết hợp với trồng lúa" if "tôm" in content else "Phản hồi mặc định"
