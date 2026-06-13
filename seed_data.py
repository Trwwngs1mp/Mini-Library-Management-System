#!/usr/bin/env python3
"""
Seed script - Add sample data for demonstration.
Run: python seed_data.py
"""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.model.database import Database
from src.controller.book_controller import BookController
from src.controller.reader_controller import ReaderController

db = Database()
book_controller = BookController(db)
reader_controller = ReaderController(db)

# ===== 100+ SÁCH THẬT =====
sample_books = [
    # Văn học Việt Nam
    {"title": "Truyện Kiều", "author": "Nguyễn Du", "isbn": "978-604-69-0001-4", "published_year": "1820", "quantity": 10},
    {"title": "Số đỏ", "author": "Vũ Trọng Phụng", "isbn": "978-604-69-1234-5", "published_year": "1936", "quantity": 5},
    {"title": "Chí Phèo", "author": "Nam Cao", "isbn": "978-604-69-0736-1", "published_year": "1941", "quantity": 8},
    {"title": "Lão Hạc", "author": "Nam Cao", "isbn": "978-604-69-0737-8", "published_year": "1943", "quantity": 6},
    {"title": "Tắt đèn", "author": "Ngô Tất Tố", "isbn": "978-604-69-0740-8", "published_year": "1937", "quantity": 7},
    {"title": "Vợ nhặt", "author": "Kim Lân", "isbn": "978-604-69-1238-3", "published_year": "1962", "quantity": 4},
    {"title": "Đất rừng phương Nam", "author": "Đoàn Giỏi", "isbn": "978-604-69-0721-7", "published_year": "1957", "quantity": 6},
    {"title": "Dế Mèn phiêu lưu ký", "author": "Tô Hoài", "isbn": "978-604-69-0735-4", "published_year": "1941", "quantity": 9},
    {"title": "Tôi thấy hoa vàng trên cỏ xanh", "author": "Nguyễn Nhật Ánh", "isbn": "978-604-1-08520-3", "published_year": "2010", "quantity": 8},
    {"title": "Mắt biếc", "author": "Nguyễn Nhật Ánh", "isbn": "978-604-1-08521-0", "published_year": "1990", "quantity": 5},
    {"title": "Cho tôi xin một vé đi tuổi thơ", "author": "Nguyễn Nhật Ánh", "isbn": "978-604-1-08522-7", "published_year": "2008", "quantity": 6},
    {"title": "Ngồi khóc trên cây", "author": "Nguyễn Nhật Ánh", "isbn": "978-604-1-08523-4", "published_year": "2013", "quantity": 4},
    {"title": "Cô gái đến từ hôm qua", "author": "Nguyễn Nhật Ánh", "isbn": "978-604-1-08524-1", "published_year": "1999", "quantity": 5},
    {"title": "Nỗi buồn chiến tranh", "author": "Bảo Ninh", "isbn": "978-604-69-1235-2", "published_year": "1987", "quantity": 3},
    {"title": "Bỉ vỏ", "author": "Nguyên Hồng", "isbn": "978-604-69-1236-9", "published_year": "1938", "quantity": 4},

    # Văn học nước ngoài
    {"title": "Nhà giả kim", "author": "Paulo Coelho", "isbn": "978-0-06-250217-4", "published_year": "1988", "quantity": 10},
    {"title": "Harry Potter và Hòn đá Phù thủy", "author": "J.K. Rowling", "isbn": "978-0-7475-3269-9", "published_year": "1997", "quantity": 8},
    {"title": "Harry Potter và Phòng chứa bí mật", "author": "J.K. Rowling", "isbn": "978-0-7475-3849-3", "published_year": "1998", "quantity": 7},
    {"title": "Harry Potter và Tên tù nhân ngục Azkaban", "author": "J.K. Rowling", "isbn": "978-0-7475-4215-5", "published_year": "1999", "quantity": 6},
    {"title": "1984", "author": "George Orwell", "isbn": "978-0-452-28423-4", "published_year": "1949", "quantity": 8},
    {"title": "Trại súc vật", "author": "George Orwell", "isbn": "978-0-452-28424-1", "published_year": "1945", "quantity": 5},
    {"title": "Chiến tranh và Hòa bình", "author": "Leo Tolstoy", "isbn": "978-0-19-923276-5", "published_year": "1869", "quantity": 3},
    {"title": "Anna Karenina", "author": "Leo Tolstoy", "isbn": "978-0-14-303500-8", "published_year": "1877", "quantity": 4},
    {"title": "Đồi gió hú", "author": "Emily Brontë", "isbn": "978-0-14-143955-6", "published_year": "1847", "quantity": 4},
    {"title": "Kiêu hãnh và Định kiến", "author": "Jane Austen", "isbn": "978-0-14-143951-8", "published_year": "1813", "quantity": 5},
    {"title": "Đà điểu và Nhà văn", "author": "Haruki Murakami", "isbn": "978-4-10-353410-7", "published_year": "1987", "quantity": 4},
    {"title": "Rừng Nauy", "author": "Haruki Murakami", "isbn": "978-4-10-100205-1", "published_year": "1987", "quantity": 5},
    {"title": "Tội ác và Hình phạt", "author": "Fyodor Dostoevsky", "isbn": "978-0-14-044913-6", "published_year": "1866", "quantity": 4},
    {"title": "Anh em nhà Karamazov", "author": "Fyodor Dostoevsky", "isbn": "978-0-14-044924-2", "published_year": "1880", "quantity": 3},
    {"title": "Bá tước Monte Cristo", "author": "Alexandre Dumas", "isbn": "978-0-14-044926-6", "published_year": "1844", "quantity": 3},
    {"title": "Ba người lính ngự lâm", "author": "Alexandre Dumas", "isbn": "978-0-14-044925-9", "published_year": "1844", "quantity": 4},
    {"title": "Phía Tây không có gì lạ", "author": "Erich Maria Remarque", "isbn": "978-0-449-21394-3", "published_year": "1929", "quantity": 3},
    {"title": "Cuốn theo chiều gió", "author": "Margaret Mitchell", "isbn": "978-0-446-36538-3", "published_year": "1936", "quantity": 5},
    {"title": "Ông già và biển cả", "author": "Ernest Hemingway", "isbn": "978-0-684-80122-3", "published_year": "1952", "quantity": 6},
    {"title": "Chuông nguyện hồn ai", "author": "Ernest Hemingway", "isbn": "978-0-684-80123-0", "published_year": "1940", "quantity": 3},
    {"title": "Kafka bên bờ biển", "author": "Haruki Murakami", "isbn": "978-4-10-100206-8", "published_year": "2002", "quantity": 4},
    {"title": "Sherlock Holmes - Toàn tập", "author": "Arthur Conan Doyle", "isbn": "978-0-14-043774-4", "published_year": "1892", "quantity": 5},
    {"title": "Chạng vạng", "author": "Stephenie Meyer", "isbn": "978-0-316-16017-9", "published_year": "2005", "quantity": 6},
    {"title": "Chúa tể những chiếc nhẫn: Nhà hobbit", "author": "J.R.R. Tolkien", "isbn": "978-0-545-01122-1", "published_year": "1937", "quantity": 5},
    {"title": "Chúa tể những chiếc nhẫn: Hai tòa tháp", "author": "J.R.R. Tolkien", "isbn": "978-0-545-01123-8", "published_year": "1954", "quantity": 4},

    # Sách kỹ năng - Phát triển bản thân
    {"title": "Đắc nhân tâm", "author": "Dale Carnegie", "isbn": "978-0-671-02703-4", "published_year": "1936", "quantity": 10},
    {"title": "Trí tuệ Do Thái", "author": "Eran Katz", "isbn": "978-604-1-09176-4", "published_year": "2008", "quantity": 5},
    {"title": "Nhà đầu tư thông minh", "author": "Benjamin Graham", "isbn": "978-0-06-055566-5", "published_year": "1949", "quantity": 4},
    {"title": "Cha giàu cha nghèo", "author": "Robert Kiyosaki", "isbn": "978-0-446-67745-5", "published_year": "1997", "quantity": 8},
    {"title": "Bí mật Dotcom", "author": "Brian Tracy", "isbn": "978-0-307-58992-9", "published_year": "2016", "quantity": 5},
    {"title": "Người giàu nhất thành Babylon", "author": "George S. Clason", "isbn": "978-0-451-58776-5", "published_year": "1926", "quantity": 6},
    {"title": "7 Thói quen của bạn trẻ thành đạt", "author": "Sean Covey", "isbn": "978-0-684-85668-1", "published_year": "1998", "quantity": 7},
    {"title": "Đừng bao giờ đi ăn một mình", "author": "Keith Ferrazzi", "isbn": "978-0-385-52378-9", "published_year": "2005", "quantity": 4},
    {"title": "Nói sao cho đúng", "author": "Marshall Rosenberg", "isbn": "978-1-892005-28-0", "published_year": "2003", "quantity": 5},
    {"title": "Tư duy nhanh và chậm", "author": "Daniel Kahneman", "isbn": "978-0-374-53355-7", "published_year": "2011", "quantity": 4},
    {"title": "Sức mạnh của thói quen", "author": "Charles Duhigg", "isbn": "978-0-8129-8160-5", "published_year": "2012", "quantity": 5},
    {"title": "Điều kỳ diệu của thái độ sống", "author": "Og Mandino", "isbn": "978-0-553-28657-5", "published_year": "1968", "quantity": 4},
    {"title": "Đời ngắn đừng ngủ dài", "author": "Robin Sharma", "isbn": "978-604-77-1983-3", "published_year": "2010", "quantity": 6},
    {"title": "Hành trình về phương Đông", "author": "Nguyên Phong", "isbn": "978-604-77-3819-3", "published_year": "2000", "quantity": 5},
    {"title": "Hành trình đi tìm Lẽ phải", "author": "Michael Sandel", "isbn": "978-0-374-53250-5", "published_year": "2009", "quantity": 3},

    # Khoa học - Công nghệ
    {"title": "Clean Code", "author": "Robert C. Martin", "isbn": "978-0-13-235088-4", "published_year": "2008", "quantity": 5},
    {"title": "Clean Architecture", "author": "Robert C. Martin", "isbn": "978-0-13-449416-6", "published_year": "2017", "quantity": 4},
    {"title": "Design Patterns", "author": "Gang of Four", "isbn": "978-0-201-63361-0", "published_year": "1994", "quantity": 3},
    {"title": "The Pragmatic Programmer", "author": "Andrew Hunt", "isbn": "978-0-201-61622-4", "published_year": "1999", "quantity": 4},
    {"title": "Introduction to Algorithms", "author": "Thomas H. Cormen", "isbn": "978-0-262-03384-8", "published_year": "1990", "quantity": 3},
    {"title": "Sapiens: Lược sử loài người", "author": "Yuval Noah Harari", "isbn": "978-0-06-231611-0", "published_year": "2011", "quantity": 7},
    {"title": "Những tấm lòng cao cả", "author": "Edmondo De Amicis", "isbn": "978-604-69-1233-8", "published_year": "1886", "quantity": 5},
    {"title": "Lược sử thời gian", "author": "Stephen Hawking", "isbn": "978-0-553-34614-5", "published_year": "1988", "quantity": 4},
    {"title": "Vũ trụ trong một vỏ hạt", "author": "Stephen Hawking", "isbn": "978-0-553-80202-5", "published_year": "2001", "quantity": 3},
    {"title": "Nguồn gốc các loài", "author": "Charles Darwin", "isbn": "978-0-14-043912-0", "published_year": "1859", "quantity": 3},
    {"title": "Tôi tài giỏi, bạn cũng thế", "author": "Adam Khoo", "isbn": "978-981-04-4631-2", "published_year": "2004", "quantity": 6},

    # Sách thiếu nhi & Tuổi teen
    {"title": "Hoàng tử bé", "author": "Antoine de Saint-Exupéry", "isbn": "978-0-15-601219-5", "published_year": "1943", "quantity": 10},
    {"title": "Khu vườn bí mật", "author": "Frances Hodgson Burnett", "isbn": "978-0-14-062076-4", "published_year": "1911", "quantity": 5},
    {"title": "Wonder - Điều kỳ diệu", "author": "R.J. Palacio", "isbn": "978-0-375-86902-0", "published_year": "2012", "quantity": 6},
    {"title": "Nhóc Nicolas", "author": "René Goscinny", "isbn": "978-0-14-038519-6", "published_year": "1959", "quantity": 4},
    {"title": "Tom Sawyer", "author": "Mark Twain", "isbn": "978-0-14-303956-3", "published_year": "1876", "quantity": 5},
    {"title": "Alice ở xứ sở thần tiên", "author": "Lewis Carroll", "isbn": "978-0-14-143976-1", "published_year": "1865", "quantity": 6},
    {"title": "Pinocchio", "author": "Carlo Collodi", "isbn": "978-0-14-243707-8", "published_year": "1883", "quantity": 5},
    {"title": "Cây cam ngọt của tôi", "author": "José Mauro de Vasconcelos", "isbn": "978-604-1-09876-3", "published_year": "1968", "quantity": 7},
    {"title": "Cậu bé mặc Pyjama sọc", "author": "John Boyne", "isbn": "978-0-385-75105-2", "published_year": "2006", "quantity": 5},

    # Tiểu thuyết kinh dị - Trinh thám
    {"title": "Mật mã Da Vinci", "author": "Dan Brown", "isbn": "978-0-385-50420-7", "published_year": "2003", "quantity": 7},
    {"title": "Thiên thần Quỷ ám", "author": "Dan Brown", "isbn": "978-0-385-51322-3", "published_year": "2009", "quantity": 5},
    {"title": "Biểu tượng thất lạc", "author": "Dan Brown", "isbn": "978-0-385-50422-1", "published_year": "2013", "quantity": 4},
    {"title": "Kẻ săn đuổi", "author": "John Grisham", "isbn": "978-0-385-51766-5", "published_year": "1991", "quantity": 4},
    {"title": "Bên bờ vực thẳm", "author": "Gillian Flynn", "isbn": "978-0-307-58837-3", "published_year": "2012", "quantity": 5},
    {"title": "Cô gái trong lồng", "author": "Jussi Adler-Olsen", "isbn": "978-0-14-312839-7", "published_year": "2007", "quantity": 4},
    {"title": "Kẻ thứ ba", "author": "Graham Greene", "isbn": "978-0-14-028567-9", "published_year": "1949", "quantity": 3},
    {"title": "Án mạng trên sông Nile", "author": "Agatha Christie", "isbn": "978-0-00-711931-0", "published_year": "1937", "quantity": 5},
    {"title": "Án mạng ở chòi số 11", "author": "Agatha Christie", "isbn": "978-0-00-711932-7", "published_year": "1935", "quantity": 4},
    {"title": "Vụ án phương Đông", "author": "Agatha Christie", "isbn": "978-0-00-711933-4", "published_year": "1934", "quantity": 4},
    {"title": "Mười người da đen nhỏ", "author": "Agatha Christie", "isbn": "978-0-00-711930-3", "published_year": "1939", "quantity": 6},

    # Kinh tế - Chính trị - Xã hội
    {"title": "Tư bản - Phê phán kinh tế chính trị", "author": "Karl Marx", "isbn": "978-0-14-044568-8", "published_year": "1867", "quantity": 3},
    {"title": "Bàn về tinh thần pháp luật", "author": "Montesquieu", "isbn": "978-0-521-36944-4", "published_year": "1748", "quantity": 2},
    {"title": "Khế ước xã hội", "author": "Jean-Jacques Rousseau", "isbn": "978-0-14-044201-4", "published_year": "1762", "quantity": 3},
    {"title": "Quốc gia giàu nhất thế giới", "author": "Thomas Sowell", "isbn": "978-0-465-08162-0", "published_year": "1998", "quantity": 3},
    {"title": "Lược sử kinh tế học", "author": "Niall Kishtainy", "isbn": "978-0-19-968054-2", "published_year": "2017", "quantity": 4},
    {"title": "Hành tinh của chúng ta", "author": "Al Gore", "isbn": "978-0-385-52271-3", "published_year": "2006", "quantity": 2},

    # Văn học đương đại - Tiếng Việt
    {"title": "Cánh đồng bất tận", "author": "Nguyễn Ngọc Tư", "isbn": "978-604-69-1237-6", "published_year": "2005", "quantity": 5},
    {"title": "Thương nhớ ở ai", "author": "Nguyễn Ngọc Tư", "isbn": "978-604-69-1238-3", "published_year": "2007", "quantity": 4},
    {"title": "Người đàn bà đi chợ", "author": "Nguyễn Ngọc Tư", "isbn": "978-604-69-1239-0", "published_year": "2011", "quantity": 3},
    {"title": "Hà Nội băm sáu phố phường", "author": "Thạch Lam", "isbn": "978-604-69-1240-6", "published_year": "1941", "quantity": 4},
    {"title": "Những ngọn nến trong đêm", "author": "Lê Minh Khuê", "isbn": "978-604-69-1241-3", "published_year": "1984", "quantity": 3},
    {"title": "Thời xa vắng", "author": "Lê Lựu", "isbn": "978-604-69-1242-0", "published_year": "1986", "quantity": 4},
    {"title": "Bến không chồng", "author": "Dương Hướng", "isbn": "978-604-69-1243-7", "published_year": "1990", "quantity": 3},
    {"title": "Mảnh đất lắm người nhiều ma", "author": "Nguyễn Khắc Trường", "isbn": "978-604-69-1244-4", "published_year": "1991", "quantity": 2},
    {"title": "Giông tố", "author": "Vũ Trọng Phụng", "isbn": "978-604-69-1245-1", "published_year": "1936", "quantity": 4},
    {"title": "Làm đĩ", "author": "Vũ Trọng Phụng", "isbn": "978-604-69-1246-8", "published_year": "1936", "quantity": 3},

    # Thơ ca
    {"title": "Thơ Hồ Chí Minh", "author": "Hồ Chí Minh", "isbn": "978-604-69-1247-5", "published_year": "1960", "quantity": 6},
    {"title": "Thơ Nguyễn Bính", "author": "Nguyễn Bính", "isbn": "978-604-69-1248-2", "published_year": "1940", "quantity": 4},
    {"title": "Thơ Xuân Diệu", "author": "Xuân Diệu", "isbn": "978-604-69-1249-9", "published_year": "1938", "quantity": 5},
    {"title": "Thơ Hàn Mặc Tử", "author": "Hàn Mặc Tử", "isbn": "978-604-69-1250-5", "published_year": "1940", "quantity": 4},
    {"title": "Thơ Tố Hữu", "author": "Tố Hữu", "isbn": "978-604-69-1251-2", "published_year": "1946", "quantity": 5},
    {"title": "Thơ Puskin", "author": "Alexander Pushkin", "isbn": "978-0-14-044787-3", "published_year": "1820", "quantity": 3},
]

# ===== 50+ ĐỘC GIẢ =====
sample_readers = [
    # Họ Nguyễn (10)
    {"name": "Nguyễn Văn An", "email": "annguyen@gmail.com", "phone": "0901234501"},
    {"name": "Nguyễn Thị Bích", "email": "bichnguyen@gmail.com", "phone": "0901234502"},
    {"name": "Nguyễn Công Cường", "email": "cuongnc@gmail.com", "phone": "0901234503"},
    {"name": "Nguyễn Thị Dung", "email": "dungnt@gmail.com", "phone": "0901234504"},
    {"name": "Nguyễn Văn Đạt", "email": "datnv@gmail.com", "phone": "0901234505"},
    {"name": "Nguyễn Minh Hạnh", "email": "hanhnm@gmail.com", "phone": "0901234506"},
    {"name": "Nguyễn Quốc Huy", "email": "huynq@gmail.com", "phone": "0901234507"},
    {"name": "Nguyễn Thị Kim", "email": "kimnt@gmail.com", "phone": "0901234508"},
    {"name": "Nguyễn Văn Long", "email": "longnv@gmail.com", "phone": "0901234509"},
    {"name": "Nguyễn Thị Mai", "email": "maint@gmail.com", "phone": "0901234510"},

    # Họ Trần (8)
    {"name": "Trần Văn Bình", "email": "binhtv@gmail.com", "phone": "0901234511"},
    {"name": "Trần Thị Hà", "email": "hatt@gmail.com", "phone": "0901234512"},
    {"name": "Trần Minh Hiếu", "email": "hieutm@gmail.com", "phone": "0901234513"},
    {"name": "Trần Thị Hương", "email": "huongtt@gmail.com", "phone": "0901234514"},
    {"name": "Trần Văn Khánh", "email": "hanhtv@gmail.com", "phone": "0901234515"},
    {"name": "Trần Thị Lan", "email": "lantt@gmail.com", "phone": "0901234516"},
    {"name": "Trần Văn Mạnh", "email": "manhtv@gmail.com", "phone": "0901234517"},
    {"name": "Trần Thị Ngọc", "email": "ngoctt@gmail.com", "phone": "0901234518"},

    # Họ Lê (7)
    {"name": "Lê Văn Anh", "email": "anhlv@gmail.com", "phone": "0901234519"},
    {"name": "Lê Thị Chi", "email": "chitl@gmail.com", "phone": "0901234520"},
    {"name": "Lê Minh Đức", "email": "duclm@gmail.com", "phone": "0901234521"},
    {"name": "Lê Thị Giang", "email": "giangtl@gmail.com", "phone": "0901234522"},
    {"name": "Lê Văn Hải", "email": "hailv@gmail.com", "phone": "0901234523"},
    {"name": "Lê Thị Hảo", "email": "haotl@gmail.com", "phone": "0901234524"},
    {"name": "Lê Văn Hoàng", "email": "hoanglv@gmail.com", "phone": "0901234525"},

    # Họ Phạm (6)
    {"name": "Phạm Văn Đô", "email": "dopv@gmail.com", "phone": "0901234526"},
    {"name": "Phạm Thị Hồng", "email": "hongpt@gmail.com", "phone": "0901234527"},
    {"name": "Phạm Minh Huy", "email": "huypm@gmail.com", "phone": "0901234528"},
    {"name": "Phạm Thị Lý", "email": "lypt@gmail.com", "phone": "0901234529"},
    {"name": "Phạm Văn Minh", "email": "minhpv@gmail.com", "phone": "0901234530"},
    {"name": "Phạm Thị Nga", "email": "ngapt@gmail.com", "phone": "0901234531"},

    # Họ Hoàng (5)
    {"name": "Hoàng Văn Bảo", "email": "baohv@gmail.com", "phone": "0901234532"},
    {"name": "Hoàng Thị Cúc", "email": "cucht@gmail.com", "phone": "0901234533"},
    {"name": "Hoàng Minh Đức", "email": "duchm@gmail.com", "phone": "0901234534"},
    {"name": "Hoàng Văn Hùng", "email": "hunghv@gmail.com", "phone": "0901234535"},
    {"name": "Hoàng Thị Phương", "email": "phuonght@gmail.com", "phone": "0901234536"},

    # Họ Vũ (5)
    {"name": "Vũ Văn Cảnh", "email": "canhvv@gmail.com", "phone": "0901234537"},
    {"name": "Vũ Thị Duyên", "email": "duyenvt@gmail.com", "phone": "0901234538"},
    {"name": "Vũ Văn Kiên", "email": "kienvv@gmail.com", "phone": "0901234539"},
    {"name": "Vũ Thị Ly", "email": "lyvt@gmail.com", "phone": "0901234540"},
    {"name": "Vũ Minh Tâm", "email": "tamvm@gmail.com", "phone": "0901234541"},

    # Họ Đỗ (4)
    {"name": "Đỗ Văn Anh", "email": "anhdv@gmail.com", "phone": "0901234542"},
    {"name": "Đỗ Thị Bình", "email": "binhdt@gmail.com", "phone": "0901234543"},
    {"name": "Đỗ Văn Chung", "email": "chungdv@gmail.com", "phone": "0901234544"},
    {"name": "Đỗ Thị Dịu", "email": "diudt@gmail.com", "phone": "0901234545"},

    # Họ khác (5)
    {"name": "Bùi Văn Huy", "email": "huibv@gmail.com", "phone": "0901234546"},
    {"name": "Đặng Thị Lan", "email": "landt@gmail.com", "phone": "0901234547"},
    {"name": "Dương Văn Nam", "email": "namdv@gmail.com", "phone": "0901234548"},
    {"name": "Hồ Văn Phát", "email": "phathv@gmail.com", "phone": "0901234549"},
    {"name": "Cao Thị Quỳnh", "email": "quynhct@gmail.com", "phone": "0901234550"},
]


def seed():
    print("=" * 60)
    print("  🌱 MINI LIBRARY - SEED DATA GENERATOR")
    print("=" * 60)

    print(f"\n📚 Đang thêm {len(sample_books)} sách...")
    success_books = 0
    fail_books = 0
    for book in sample_books:
        result = book_controller.add_book(
            title=book["title"],
            author=book["author"],
            isbn=book["isbn"],
            published_year=book["published_year"],
            quantity=str(book["quantity"]),
        )
        if result["success"]:
            success_books += 1
        else:
            fail_books += 1
            print(f"  ❌ {book['title']}: {', '.join(result['errors'])}")

    print(f"\n👤 Đang thêm {len(sample_readers)} độc giả...")
    success_readers = 0
    fail_readers = 0
    for reader in sample_readers:
        result = reader_controller.add_reader(
            name=reader["name"],
            email=reader["email"],
            phone=reader["phone"],
        )
        if result["success"]:
            success_readers += 1
        else:
            fail_readers += 1

    print("\n" + "=" * 60)
    print("  ✅ KẾT QUẢ:")
    print(f"     📚 Sách: {success_books}/{len(sample_books)} thành công" +
          (f" ({fail_books} lỗi)" if fail_books else ""))
    print(f"     👤 Độc giả: {success_readers}/{len(sample_readers)} thành công" +
          (f" ({fail_readers} lỗi)" if fail_readers else ""))
    print(f"\n     Tổng cộng: {success_books + success_readers} bản ghi đã được thêm!")
    print("=" * 60)
    print("\n💡 Chạy ứng dụng: python web_app.py")
    print("💡 Mở trình duyệt: http://localhost:5000")

    db.close()


if __name__ == "__main__":
    seed()