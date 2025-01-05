from flask import Flask, request, jsonify
from agent.MultiAgent import MultiAgentShrimpRetrievalSystem
from contextual_retrieval.ContextualRetrieval import ContextualRetrieval
from flask_cors import CORS

from dotenv import load_dotenv
import os

load_dotenv()
os.environ['KMP_DUPLICATE_LIB_OK']='True'

app = Flask(__name__)
CORS(app)


cr = ContextualRetrieval()
    
document = """
                Nguyên nhân và biểu hiện của bệnh đốm trắng ở tôm:
                Do thời tiết bất thường, vùng nuôi ô nhiễm là nguyên nhân chính gây nên bệnh đốm trắng trên tôm. Khi ao nuôi xuất hiện dịch bệnh này. Người nuôi cần có phương án xử lý thích hợp để tiêu diệt mầm bệnh, tránh lây lan.

                Theo các nhà khoa học, tác nhân gây ra bệnh đốm trắng ở tôm bao gồm virus hoặc vi khuẩn gây ra. Bệnh thường có tốc độ lây lan rất nhanh và mức độ gây hại rất lớn. Thời gian gây bệnh thường từ tháng nuôi thứ hai trở đi. Khi mà lượng chất thải nuôi tôm bắt đầu xuất hiện nhiều. Môi trường nước ao bị ô nhiễm, gây stress cho tôm. Mầm bệnh có thể đã ủ trong tôm hoặc xâm nhập từ bên ngoài vào qua nguồn nước. Hoặc các loại ký chủ trung gian (cua, còng, cáy, chim..). Khi gặp thời thiết thay đổi sẽ tạo điều kiện cho các loại virus, vi khuẩn bùng phát gây ra dịch bệnh cho tôm.

                Biểu hiện
                Bệnh đốm trắng ở tôm do virus gây ra (White Spot Syndrome Virus – WSSV): tôm có biểu hiện hoạt động kém. Ăn nhiều đột ngột sau đó bỏ ăn. Bơi lờ đờ ở mặt nước hay dạt vào bờ. Quan sát vỏ tôm có nhiều đốm trắng ở giáp đầu ngực, đốt bụng thứ 5, 6 và lan toàn thân. Đôi khi tôm cũng có dấu hiệu đỏ thân. Khi các đốm trắng xuất hiện, sau 3 – 10 ngày tôm chết hàng loạt với tỉ lệ chết cao và nhanh.
                Bệnh do vi khuẩn gây ra (Bacteria White Spot Syndrome – BWSS): khi mới nhiễm khuẩn tôm vẫn ăn mồi, lột xác và chưa thấy các đốm trắng trên tôm. Tuy nhiên, quá trình lột xác bị chậm lại, tôm chậm lớn. Khi bệnh nặng, tôm không chết hàng loạt mà sẽ chết rải rác, hầu hết tôm bị đóng rong, mang bị bẩn. Lúc này quan sát tôm mới thấy các đốm trắng mờ đục hình tròn nhỏ trên vỏ khắp cơ thể.
                Phòng ngừa và xử lý bệnh đốm trắng ở tôm:
                Đối với ao chưa bị bệnh
                Ngừa bệnh bằng cách sử dụng chế phẩm EM thứ cấp (hoạt hóa từ EM1):

                Xử lý đáy, ao trước khi thả
                Tạt chế phẩm EM thường xuyên trong suốt quá trình nuôi tôm.
                Một khi các vi sinh vật có lợi phát triển mạnh. Chúng tiêu diệt các vi sinh vật có hại, vi khuẩn có hại =>giúp phòng bệnh tốt hơn.

                Người nuôi cần thường xuyên nắm bắt các thông tin về diễn biến dịch bệnh tại địa phương. Để có biện pháp phòng ngừa thích hợp. Khi vùng nuôi đã xuất hiện dịch bệnh mà ao nuôi nhà mình chưa có biểu hiện dịch bệnh.

                Các hộ nuôi nên xử lý bằng các biện pháp sau:
                Không nên đến nơi phát dịch, hạn chế người qua lại các ao tôm. Trường hợp phải vào ao thì cần thay quần áo và lội qua bể nước khử trùng (Chlorine, formol 5%).
                Sử dụng vôi bột (CaO) rải xung quanh bờ ao, đắp chặt cống cấp và thoát nước. Quây lưới quanh bờ ao để ngăn chặn xâm nhập của cua, còng, cá… vào ao. Căng dây và lắp hình nộm để chống chim cò vào ao.
                Hạn chế thay nước ao. Kiểm tra các yếu tố môi trường ao nuôi để điều chỉnh kịp thời như tăng cường quạt khí, xiphông đáy ao, ổn định pH, độ kiềm. Đồng thời tăng cường bổ sung Vitamin C, men vi sinh, khoáng Trường Sinh, thuốc bổ gan (TS 1001 của Trường Sinh), vi lượng vào thức ăn nhằm tăng sức đề kháng cho tôm. Nếu nước ao có màu trà đậm, kiểm tra thấy lượng Vibrio trong nước tăng vượt ngưỡng thì nên khử trùng nước ao bằng TS B52, SDK… Sau đó, phải bón ngay chế phẩm vi sinh để phục hồi lượng vi khuẩn có lợi trong ao. Thường xuyên kiểm tra sức ăn của tôm trong nhá, vó để điều chỉnh thức ăn phù hợp.
                Đối với ao bị bệnh
                Cách xử lý khi phát hiện có dấu hiệu nghi ngờ bệnh đốm trắng (một vài con tấp bờ) nhanh chóng vớt ra khỏi ao. Dùng SDK diệt khuẩn 1lít/1000m3 nước. Oxyxanhletomine 1,5kg/1000m3 nước đánh vào ao. Sau 2 giờ đánh TS 1001 liều dùng 2 lít/1000m3nước + Bet-to-gane 2 lít/1000m3 nước kết hợp cho ăn TS 1001 liều cao 5 lần/ngày. Liều dùng:  0,5 lít/10kg thức ăn, cho ăn ngày 3 cữ.

                Để chặn đứng virus đốm trắng không cho bùng phát khắp ao, tăng cường sức khỏe cho tôm bằng Vitamin C.

                Xử lý môi trường bằng cách dùng TS B52 buổi sáng, buổi chiều dùng Zeo bột để lắng lọc nước hôm sau xử lý đáy bằng men vi sinh Hatico.s liều cao để giúp vi sinh vật có lợi phát triển, giúp tôm khỏe nhanh hồi phục. Sự kết hợp trên sẽ tăng cường sức đề kháng cơ thể cho tôm đồng thời làm suy yếu giảm sự phát triển virus.
                """

contextualized_chunks = cr.process_document(document)
# print(contextualized_chunks)
cr.create_retrievers(contextualized_chunks)
    
cnn_model_path = './models/cnn/VGG16.keras'
fasttext_model_path = './models/fasttext/fasttext_model.bin'
multi_agent_system = MultiAgentShrimpRetrievalSystem(cr, cnn_model_path=cnn_model_path, fasttext_model_path=fasttext_model_path, max_history=3)

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
        try:
            images = latest_message.get("images", [])
            img_pth = images[0].get('url')
        except:
            img_pth = None
        try:
            if text:
                bot_response = self.generate_bot_response(text)
            elif captions:
                print(f"Link ảnh: {images[0].get('url')}")
                bot_response = self.generate_bot_response(captions, image_path=img_pth)
            elif img_pth:
                captions = "Giải thích hình sau"
                bot_response = self.generate_bot_response(captions, image_path=img_pth)    
            else:
                return jsonify({"error": "Each message must have either 'text' or 'captions'."}), 400
        except Exception as e:
            return jsonify({
                "message": "Fail",
                "answer": str(e),
                "success": False
            }), 500
        return jsonify({
            "message": "successful",
            "answer": bot_response,
            "success": True
        }), 200

    def generate_bot_response(self, content, image_path=None):
        return multi_agent_system.process_query(content, image_path)

send_message_api = SendMessageAPI()

@app.route('/api/v1/messages/send', methods=['POST'])
def send_message():
    return send_message_api.post()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
