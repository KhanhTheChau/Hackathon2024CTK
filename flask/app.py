from flask import Flask, request, jsonify

from flask_cors import CORS
app = Flask(__name__)
CORS(app)


class SendMessageAPI:
    def post(self):
        data = request.json
        messages = data.get("messages", [])

        # Kiểm tra tính hợp lệ của dữ liệu
        if not messages or not isinstance(messages, list):
            return jsonify({"error": "Field 'messages' must be a non-empty list."}), 400

        # Lấy tin nhắn mới nhất từ cuối mảng
        latest_message = messages[-1]

        captions = latest_message.get("captions")
        text = latest_message.get("text")

        if text:
            bot_response = self.generate_bot_response(text)
        elif captions:
            bot_response = self.generate_bot_response(captions)
        else:
            return jsonify({"error": "Each message must have either 'text' or 'captions'."}), 400

        return jsonify({
            "message": "successful",
            "answer": bot_response,
            "success": True
        }), 200

    def generate_bot_response(self, content):
        return "Chưa có câu trả lời, tạm dị đi"

send_message_api = SendMessageAPI()

@app.route('/api/v1/messages/send', methods=['POST'])
def send_message():
    return send_message_api.post()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
