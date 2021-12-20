from dotenv import load_dotenv
from tkinter.ttk import Combobox
from tkinterhtml import HtmlFrame
from os import path, remove, environ
from tkinter import Tk, Label, Button, Entry, Toplevel, Frame
from Process import main_process, get_subjects, get_exams, get_week, decode_pwd


def check_login(entry_usr: str, entry_pwd: str):
    usr, pwd = entry_usr.get(), entry_pwd.get()
    lst_year, lst_semester = main_process(usr, pwd)

    if lst_year is None or lst_semester is None:
        remove('./user_info.env')  # xóa file chứa tài khoản sai
        lbl_error = Label(frame, text='Tài khoản hoặc mật khẩu sai!\nVui lòng đăng nhập lại.', fg='red')
        lbl_error.grid(row=5, columnspan=2)

        return

    frame.destroy()
    main_page()


def login_form():
    global frame

    frame = Frame(app, width=w, height=h)
    frame.grid()
    app.title('Đăng nhập')

    lbl_app = Label(frame, text='Đăng Nhập', font='Times 20')
    lbl_app.grid(row=0, columnspan=2, padx=50)

    lbl_usr = Label(frame, text='Tài Khoản:')
    entry_usr = Entry(frame, width=20)

    lbl_usr.grid(row=2, column=0, sticky='E')
    entry_usr.grid(row=2, column=1, sticky='W')

    lbl_pwd = Label(frame, text='Mật Khẩu:')
    entry_pwd = Entry(frame, show='*', width=20)

    lbl_pwd.grid(row=3, column=0, sticky='E')
    entry_pwd.grid(row=3, column=1, sticky='W')

    btn_login = Button(frame, text='Đăng nhập', command=lambda: check_login(entry_usr, entry_pwd))
    btn_login.grid(row=4, columnspan=2, pady=10)


def schedule_page(url, menu_year, menu_semester):
    schedule_app = Toplevel()

    w, h = 1350, 850
    center_screen = f'{ w }x{ h }+{ sc_w // 2 - w // 2 }+{ sc_h // 2 - h // 2 }'  # cho hiển thị mặc định ở giữa màn hình

    schedule_app.wm_geometry(center_screen)
    schedule_app.wm_title("Lịch học")

    year, semester = menu_year.get(), menu_semester.get()
    lst_week = get_week(year, semester)

    menu_week = Combobox(schedule_app, width=10)
    menu_week['values'] = lst_week
    menu_week.current(0)
    menu_week.place(x=0, y=0)

    def show(event):
        week = menu_week.get()

        frame_schedule = HtmlFrame(schedule_app, horizontal_scrollbar="auto")
        html_schedule = get_subjects(url, year, semester, week)

        frame_schedule.set_content(html_schedule)
        frame_schedule.place(x=0, y=30, width=w, height=h)

    menu_week.bind("<<ComboboxSelected>>", show)


def exam_page(url, menu_year, menu_semester):
    exam_app = Toplevel()

    w, h = 1200, 500
    center_screen = f'{ w }x{ h }+{ sc_w // 2 - w // 2 }+{ sc_h // 2 - h // 2 }'  # cho hiển thị mặc định ở giữa màn hình

    exam_app.wm_geometry(center_screen)
    exam_app.wm_title("Lịch thi")

    year, semester = menu_year.get(), menu_semester.get()

    frame_exam = HtmlFrame(exam_app, horizontal_scrollbar="auto")
    html_exam = get_exams(url, year, semester)

    frame_exam.set_content(html_exam)
    frame_exam.place(x=0, y=0, width=w, height=h)


def logout():
    remove('./user_info.env')
    frame_main_page.destroy()
    login_form()


def main_page():
    global frame_main_page

    url = 'https://online.vlu.edu.vn/'
    app.title("Trang chủ")

    frame_main_page = Frame(app)
    frame_main_page.pack()

    load_dotenv('./user_info.env')
    usr, pwd = environ['USER_NAME'], environ['PASSWORD']

    lst_year, lst_semester = main_process(usr, decode_pwd(pwd))

    menu_year = Combobox(frame_main_page, width=10)
    menu_year['values'] = lst_year
    menu_year.current(0)
    menu_year.grid(row=0, column=0, padx=10)

    menu_semester = Combobox(frame_main_page, width=10)
    menu_semester['values'] = lst_semester
    menu_semester.current(0)
    menu_semester.grid(row=1, column=0, padx=10)

    btn_schedule = Button(frame_main_page, text='Lịch học', command=lambda: schedule_page(url, menu_year, menu_semester))
    btn_schedule.grid(row=0, column=1, pady=5)

    btn_exam = Button(frame_main_page, text='Lịch thi', command=lambda: exam_page(url, menu_year, menu_semester))
    btn_exam.grid(row=1, column=1, pady=5)

    btn_logout = Button(frame_main_page, text='Đăng xuất', command=lambda: logout())
    btn_logout.grid(row=2, columnspan=2, pady=5)


def main_gui():
    global app, w, h, center_screen, sc_w, sc_h

    app = Tk()
    w, h = 220, 170  # width và height của cửa sổ
    sc_w, sc_h = app.winfo_screenwidth(), app.winfo_screenheight()  # width và height của màn hình
    center_screen = f'{ w }x{ h }+{ sc_w // 2 - w // 2 }+{ sc_h // 2 - h // 2 }'  # cho hiển thị mặc định ở giữa màn hình

    app.title('Schedule - VLU')
    app.geometry(center_screen)
    app.maxsize(width=w, height=h)
    app.minsize(width=w, height=h)

    if not path.isfile('./user_info.env'):
        login_form()
    else:
        main_page()
    app.mainloop()


main_gui()
