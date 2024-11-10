from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_mysqldb import MySQL
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import os

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def guiThongTinDatPhong(day, date, phong_id, nguoiNhan):
    anfitrion = "smtp.gmail.com"
    puerto = 587
    diaChiNguoiGui = "lapthai03@gmail.com"
    diaChiNguoiNhan = nguoiNhan
    
    # Thiết lập máy chủ
    server = smtplib.SMTP(anfitrion, puerto)
    server.starttls()
    server.login(diaChiNguoiGui)
    
    # Nội dung email
    tieuDe = "THÔNG TIN VỀ ĐẶT PHÒNG CỦA BẠN"
    noiDung = f"Quý khách đã đặt phòng thành công tại phòng {phong_id} vào ngày {day} từ {date}. Xin cảm ơn!"
    
    # Tạo email
    email = MIMEMultipart()
    email['From'] = diaChiNguoiGui
    email['To'] = diaChiNguoiNhan
    email['Subject'] = tieuDe
    email.attach(MIMEText(noiDung, 'plain'))
    
    # Gửi email
    server.sendmail(diaChiNguoiGui, diaChiNguoiNhan, email.as_string())
    server.quit()

def guiThongBaoYeuCau(email):
    anfitrion = "smtp.gmail.com"
    puerto = 587
    diaChiNguoiGui = "youremail@gmail.com"

    
    # Thiết lập máy chủ
    server = smtplib.SMTP(anfitrion, puerto)
    server.starttls()
    server.login(diaChiNguoiGui)
    
    # Nội dung email
    tieuDe = "YÊU CẦU ĐẶT PHÒNG ĐÃ ĐƯỢC GỬI"
    noiDung = "Quý khách đã gửi yêu cầu đặt phòng thành công. Chúng tôi sẽ liên hệ qua email này để xác nhận hoặc điều chỉnh thông tin. Cảm ơn!"
    
    # Tạo email
    email = MIMEMultipart()
    email['From'] = diaChiNguoiGui
    email['To'] = email
    email['Subject'] = tieuDe
    email.attach(MIMEText(noiDung, 'plain'))
    
    # Gửi email
    server.sendmail(diaChiNguoiGui, email, email.as_string())
    server.quit()

def thongBaoChoAdmin(tenKhach, emailKhach, ngay, date, suc_chua, ly_do):
    anfitrion = "smtp.gmail.com"
    puerto = 587
    diaChiNguoiGui = "thaivietlap24@gmail.com"
    matKhauNguoiGui = "yourpassword"
    diaChiAdmin = "thaivietlap24@gmail.com"  # Địa chỉ admin
    
    # Thiết lập máy chủ
    server = smtplib.SMTP(anfitrion, puerto)
    server.starttls()
    server.login(diaChiNguoiGui, matKhauNguoiGui)
    
    # Nội dung email
    tieuDe = f"Yêu cầu đặt phòng từ khách: {tenKhach}"
    noiDung = (f"Yêu cầu đặt phòng mới từ khách hàng {tenKhach} (email: {emailKhach}). "
               f"Thời gian: {ngay} vào lúc {date}, số người tham gia: {suc_chua}. "
               f"Lý do: '{ly_do}'.")
    
    # Tạo email
    email = MIMEMultipart()
    email['From'] = diaChiNguoiGui
    email['To'] = diaChiAdmin
    email['Subject'] = tieuDe
    email.attach(MIMEText(noiDung, 'plain'))
    
    # Gửi email
    server.sendmail(diaChiNguoiGui, diaChiAdmin, email.as_string())
    server.quit()

# Hàm gửi email
def send_email(subject, to_email, message):
    anfitrion = "smtp.gmail.com"
    puerto = 587
    direccionDe = os.getenv('EMAIL_ADDRESS')  # Sử dụng biến môi trường cho địa chỉ email
    contrasenaDe = os.getenv('EMAIL_PASSWORD')  # Sử dụng biến môi trường cho mật khẩu email
    servidor = smtplib.SMTP(anfitrion, puerto)
    
    try:
        servidor.starttls()
        servidor.login(direccionDe, contrasenaDe)
        email = MIMEMultipart()  # Tạo đối tượng email
        email['From'] = direccionDe
        email['To'] = to_email
        email['Subject'] = subject
        mensaje = MIMEText(message)
        email.attach(mensaje)
        servidor.sendmail(direccionDe, to_email, email.as_string())
        print(f"Email đã gửi đến {to_email}")
    except Exception as e:
        print(f"Lỗi khi gửi email: {e}")
    finally:
        servidor.quit()

# Cấu hình ứng dụng Flask và kết nối MySQL
app = Flask(__name__)
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '123456'
app.config['MYSQL_DB'] = 'university'
db = MySQL(app)

def darHora(horaa):
    partido = str.split(horaa, "-")  # Lấy giờ bắt đầu và kết thúc
    primeraHora = partido[0]  # Giờ bắt đầu
    segundaHora = partido[1]  # Giờ kết thúc
    
    primeraFinal = primeraHora
    if '30' in primeraHora:  # Kiểm tra nếu là nửa giờ hay giờ tròn
        primeraFinal = str.split(primeraHora, ":")  # Lấy phần trước dấu ":"
        primeraFinal = primeraFinal[0] + ".5"  # Thêm ".5"
    else:
        primeraFinal = str.split(primeraHora, ":")  # Nếu không có, thì là giờ tròn
        primeraFinal = primeraFinal[0] + ".0"  # Thêm ".0"
    
    # Kiểm tra giờ kết thúc
    if '30' in segundaHora:  # Kiểm tra nếu là nửa giờ hay giờ tròn
        segundaFinal = str.split(segundaHora, ":")  # Lấy phần trước dấu ":"
        segundaFinal = segundaFinal[0] + ".5"  # Thêm ".5"
    else:
        segundaFinal = str.split(segundaHora, ":")  # Nếu không có, thì là giờ tròn
        segundaFinal = segundaFinal[0] + ".0"  # Thêm ".0"
    
    primeraNumero = float(primeraFinal)  # Chuyển đổi thành số thập phân
    segundaNumero = float(segundaFinal)  # Chuyển đổi thành số thập phân
    
    x = int((primeraNumero - 6) * 2)  # Chuyển đổi thành số nguyên
    y = int((segundaNumero - 6) * 2)  # Chuyển đổi thành số nguyên
    
    return x, y
def intermedios(a, b, aux, day, ban_giang=None, may_chieu=None):  # Thêm tham số cho ban_giang và may_chieu
    base_query = f"SELECT * FROM phong WHERE {day} = 1 AND `{a}` = 1 AND `{b}` = 1"
    
    # Xây dựng điều kiện dựa trên các đặc điểm của phòng nếu có yêu cầu
    if aux == 2:
        pass  # Không yêu cầu thêm đặc điểm nào
    elif aux == 1 and ban_giang:
        base_query += f" AND bang = '{ban_giang}'"
    elif aux == 3 and may_chieu:
        base_query += f" AND may_chieu = '{may_chieu}'"
    elif aux == 4 and ban_giang and may_chieu:
        base_query += f" AND bang = '{ban_giang}' AND may_chieu = '{may_chieu}'"
    
    # Thêm các khung giờ trung gian
    for i in range(a + 1, b):
        base_query += f" AND `{i}` = 1"
    
    print(base_query)
    return base_query



a = None
b = None
day = None
date = None
muon = None

# Khóa bí mật cho phiên
app.secret_key = "mysecretkey"
valid_emails = ["lap.2274802010473@vanlanguni.vn", "chien.2274802010071@vanlanguni.vn"]
@app.route('/')
def home():
    if 'user_id' in session:
        return render_template('home.html', user_email=session['user_id'])  # Truyền email vào template
    else:
        return redirect(url_for('login'))  # Nếu chưa đăng nhập, chuyển hướng về trang đăng nhập

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        
        # Kiểm tra email hợp lệ
        if email in valid_emails:
            # Giả sử mật khẩu đúng, bạn lưu thông tin người dùng vào session
            session['email'] = email  # Lưu email vào session
            session['user_id'] = valid_emails.index(email)  # Ví dụ lưu user_id theo index trong danh sách valid_emails
            return redirect(url_for('home'))  # Chuyển hướng đến trang home sau khi đăng nhập thành công
        else:
            return "Tài khoản không tồn tại hoặc không hợp lệ"

    return render_template('login.html')


@app.route('/index')
def index():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    # Kiểm tra sự tồn tại của khóa 'email' trong session
    if 'email' not in session:
        return redirect(url_for('login'))  # Điều hướng đến trang đăng nhập nếu không có email trong session

    return render_template('index.html', email=session['email'])


# Route cho trang yêu cầu phòng (chỉ dành cho người dùng đã đăng nhập)
@app.route('/request_hall', methods=['GET', 'POST'])
def request_hall():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        ten = request.form['ten']
        email = request.form['email']
        ngay = request.form['ngay']
        # phong_id = request.form['phong_id']
        # so_nguoi = request.form['so_nguoi']
        ly_do = request.form['ly_do']
        # Gửi email xác nhận và email cho quản trị viên
        # email_xac_nhan(email)
        # email_cho_quan_tri(ten, email, ngay, phong_id, so_nguoi, ly_do)
        return redirect(url_for('confirm_request'))
    return render_template('request_hall.html')

# Route cho trang xác nhận yêu cầu
@app.route('/confirm_request')
def confirm_request():
    return render_template('confirm_request.html')

# Route đăng xuất
@app.route('/logout')
def logout():
    session.clear()  # Xóa phiên đăng nhập
    return redirect(url_for('home'))

@app.route('/search', methods=['POST'])
def search():
    if request.method == 'POST':
        day = request.form.get('day')
        may_chieu = request.form.get('may_chieu', 'không')
        ban_giang = request.form.get('ban_giang', 'không')
        date = request.form.get('date')
        suc_chua = request.form.get('suc_chua')
        so_phong = request.form.get('so_phong')

        # Thiết lập giá trị mặc định nếu không có dữ liệu từ biểu mẫu
        if not suc_chua:
            suc_chua = 0
        if not so_phong:
            so_phong = 0

        # Thiết lập truy vấn với điều kiện tìm kiếm linh hoạt
        query = "SELECT * FROM university_booking.phong WHERE 1=1"
        if suc_chua:
            query += f" AND suc_chua >= {suc_chua}"
        if so_phong:
            query += f" AND so_phong = {so_phong}"
        if may_chieu != "không":
            query += f" AND may_chieu = '{may_chieu}'"
        if ban_giang != "không":
            query += f" AND ban_giang = '{ban_giang}'"

        cursor = db.connection.cursor()
        cursor.execute(query)
        data = cursor.fetchall()
        cursor.close()

        return render_template('search.html', datos=data)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)
