import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QListWidgetItem, QWidget, QVBoxLayout, QLabel
from PyQt6.QtGui import QPixmap
import pymysql
from form import Ui_Form


class AgentApp(QMainWindow, Ui_Form):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.db = pymysql.connect(
            host='localhost',
            user='root',
            password='',
            database='27.01'
        )
        self.cursor = self.db.cursor()


        self.current_page = 0
        self.agents_per_page = 5

        # Загрузка данных
        self.load_agents()

        # Подключение событий
        self.prev_button.clicked.connect(self.prev_page)
        self.next_button.clicked.connect(self.next_page)

    def load_agents(self):
        self.agent_list.clear()

        offset = self.current_page * self.agents_per_page
        self.cursor.execute("SELECT * FROM agent LIMIT %s OFFSET %s", (self.agents_per_page, offset))
        agents = self.cursor.fetchall()

        for agent in agents:
            item = QListWidgetItem()
            widget = QWidget()
            layout = QVBoxLayout(widget)

            type_label = QLabel(f"Тип: {agent[2]} | Наименование: {agent[1]}")
            layout.addWidget(type_label)

            phone_label = QLabel(f"Телефон: {agent[6]}")
            layout.addWidget(phone_label)

            priority_label = QLabel(f"Приоритетность: {agent[10]}")
            layout.addWidget(priority_label)


            if "\\" in agent[9]:
                image_path = agent[9].replace("\\", "/").lstrip("/")  # Исправляем путь
                photo_label = QLabel()
                print(image_path)
                pixmap = QPixmap(image_path)
                photo_label.setPixmap(pixmap)


                photo_label.setScaledContents(True)
                photo_label.setFixedSize(100, 100)

                layout.addWidget(photo_label)

            else:
                placeholder_label = QLabel()
                placeholder_label.setPixmap(QPixmap("picture.png"))
                placeholder_label.setScaledContents(True)
                placeholder_label.setFixedSize(200, 200)
                layout.addWidget(placeholder_label)

            item.setSizeHint(widget.sizeHint())
            self.agent_list.addItem(item)
            self.agent_list.setItemWidget(item, widget)

    def prev_page(self):
        if self.current_page > 0:
            self.current_page -= 1
            self.load_agents()

    def next_page(self):
        self.current_page += 1
        self.load_agents()

    def closeEvent(self, event):
        self.cursor.close()
        self.db.close()
        event.accept()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = AgentApp()
    window.show()
    sys.exit(app.exec())