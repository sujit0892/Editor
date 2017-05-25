from tkinter import *
import tkinter.filedialog
import tkinter.messagebox
from PIL import ImageTk,Image
import os
root=Tk()
root.title("editor")
root.geometry('350x350')
menu_bar=Menu(root)

show_line_no=IntVar()
themes=IntVar()
show_line_no.set(1)
show_cur=BooleanVar()
file_name=None
show_cursor=IntVar()
show_cursor.set(1)
themes=StringVar()
themes.set('Default')
color_schemes = {
'Default': '#000000.#FFFFFF',
'Greygarious':'#83406A.#D1D4D1',
'Aquamarine': '#5B8340.#D1E7E0',
'Bold Beige': '#4B4620.#FFF0E1',
'Cobalt Blue':'#ffffBB.#3333aa',
'Olive Green': '#D1E7E0.#5B8340',
'Night Mode': '#FFFFFF.#000000',
}

def cut():
   content_text.event_generate("<<Cut>>")
def copy():
   content_text.event_generate("<<Copy>>")
def paste():
   content_text.event_generate("<<Paste>>")
def redo(event=None):
    content_text.event_generate("<<Redo>>")
    return 'break'
def undo(event=None):
    content_text.event_generate("<<Undo>>")
    return 'break'

def search_text(needle, if_ignore_case, content_text, search_toplevel, search_box):
    content_text.tag_remove('match', '1.0', END)
    matches_found = 0
    if needle:
        start_pos = '1.0'
        while True:
            start_pos=content_text.search(needle,start_pos,nocase=if_ignore_case,stopindex=END)
            if not start_pos:
                break;
            end_pos='{}+{}c'.format(start_pos,len(needle))
            content_text.tag_add('match',start_pos,end_pos)
            matches_found+=1
            start_pos=end_pos
        content_text.tag_configure('match',background='yellow',foreground='red')
    search_box.focus_set()
    search_toplevel.title("{} match found".format(matches_found))   

def find_text(event=None):
    find_window=Toplevel(root)
    find_window.transient()
    find_window.resizable(False,False)
    find_window.title("find text")
    Label(find_window,text="find all :").grid(row=0,column=0,padx=2,pady=2)
    search=Entry(find_window)
    search.focus_set()
    search.grid(row=0,column=1,padx=2,pady=2)
    ignore_case_value = IntVar()
    Checkbutton(find_window,text="Ignore case",variable=ignore_case_value).grid(row=1,column=1,padx=2,pady=2,sticky=W)
    Button(find_window,text="find",command=lambda: search_text(search.get(),ignore_case_value.get(), content_text, find_window,search)).grid(row=0,column=2,padx=2,pady=2)
    def close_search_window():
       content_text.tag_remove('match', '1.0', END)
       find_window.destroy()

    find_window.protocol('WM_DELETE_WINDOW',close_search_window)
    return 'break'

def select_all(event=None):
    content_text.tag_add('sel','1.0','end')
    return 'break'

def open_file(event=None):
     input_file=tkinter.filedialog.askopenfilename(defaultextension='.txt',filetypes=[("All Files","*.*"),("Text Document","*.txt")],initialdir="/home/marinex")
     if input_file:
         global file_name
         file_name=input_file
         root.title(file_name) 
         content_text.delete('1.0',END)
         with open(file_name) as __file:
             content_text.insert('1.0',__file.read()) 
def saveas(event=None):
     input_file=tkinter.filedialog.asksaveasfilename(defaultextension='.txt',filetypes=[("All Files","*.*"),("Text Document","*.txt")],initialdir="/home/marinex")
     if input_file:
        global file_name
        file_name=input_file
        write_to_file(file_name)
        root.title("{}".format(file_name))
     return 'break' 
def save(event=None):
   global file_name
   if file_name:
      write_to_file(file_name)
   else:
      saveas()

def write_to_file(file_name):
    content=content_text.get('1.0',END)
    with open(file_name,W) as __file:
        __file.write(content)      
 
def new_file(event=None):
    global file_name
    root.title("Untitled")
    file_name=None
    content_text.delete("1.0",END)

def show_about():
    tkinter.messagebox.showinfo(title="about",message="welcome to editor\nthis is develop by sujit")   
def show_help():
    tkinter.messagebox.showinfo(title="about",message="welcome to editor\nthis is develop by sujit")

def on_content_changed(event=None):
    update_line_no()
    update_cursor_info()

def get_line_no():
    line=''
    if(show_line_no.get()):
      row,col=content_text.index("end").split(".")
      for i in range(1,int(row)):
          line+=str(i)+"\n"
    return line
       
def update_line_no():
    line_no=get_line_no()
    line_no_bar.configure(state='normal')
    line_no_bar.delete("1.0","end")
    line_no_bar.insert("1.0",line_no)
    line_no_bar.configure(state='disabled')

def highlight(interval=100):
    content_text.tag_remove("active_line",'1.0','end')
    content_text.tag_add('active_line','insert linestart','insert lineend+1c')
    content_text.after(interval,toggle_highlight)

def undo_highlight():
    content_text.tag_remove("active_line",'1.0','end')
    
def toggle_highlight():
    if show_cur.get():
      highlight()
    else:
      undo_highlight()

def show_cursor_info():
    show_cursor_info=show_cursor.get()
    if show_cursor_info:
        cursor_info.pack(expand='no',fill='none',side='right',anchor='se')
    else:
        cursor_info.pack_forget()

def update_cursor_info():
    row,col=content_text.index(INSERT).split('.')
    row_num=str(int(row))
    col_num=str(int(col)+1)
    infoText='Line : {} | Column : {}'.format(row_num,col_num)
    cursor_info.configure(text=infoText)

def change_theme():
    theme=themes.get()
    theme_choice=color_schemes.get(theme)
    fg,bg=theme_choice.split('.')
    content_text.configure(foreground=fg,background=bg)

def show_popup_menu(event):
    popup_menu.tk_popup(event.x_root, event.y_root)
#menu bar
file_menu=Menu(menu_bar,tearoff=0)
file_menu.add_command(label="New",accelerator="Ctrl+N",underline=0,command=new_file)
file_menu.add_command(label="Open",accelerator="Ctrl+O",underline=0,command=open_file)
file_menu.add_command(label="Save",accelerator="Ctrl+S",underline=0,command=save)
file_menu.add_command(label="Save As",accelerator="Shift+Ctrl+S",underline=0,command=saveas)
file_menu.add_separator()
file_menu.add_command(label="Exit",accelerator="Alt+F4",underline=0)

edit_menu=Menu(menu_bar,tearoff=0)
edit_menu.add_command(label="undo",accelerator="Ctrl+Z",command=undo)
edit_menu.add_command(label="redo",accelerator="Ctrl+Y",command=redo)
edit_menu.add_separator()
edit_menu.add_command(label="cut",accelerator="Ctrl+X",command=cut)
edit_menu.add_command(label="copy",accelerator="Ctrl+C",command=copy)
edit_menu.add_command(label="paste",accelerator="Ctrl+V",command=paste)
edit_menu.add_separator()
edit_menu.add_command(label="Find",accelerator="Ctrl+F",command=find_text)
edit_menu.add_separator()
edit_menu.add_command(label="Select All",accelerator="Ctrl+A",command=select_all)

view_menu=Menu(menu_bar,tearoff=0)
view_menu.add_checkbutton(label="show line no",variable=show_line_no,command=update_line_no)
view_menu.add_checkbutton(label="show cursor location at bottom",variable=show_cursor,command=show_cursor_info)
view_menu.add_checkbutton(label="highlight current line",onvalue=1,offvalue=0,variable=show_cur,command=toggle_highlight)
themes_menu=Menu(view_menu,tearoff=0)
themes_menu.add_radiobutton(label="Default",variable=themes,command=change_theme)
themes_menu.add_radiobutton(label="Aquamarine",variable=themes,command=change_theme)
themes_menu.add_radiobutton(label="Bold Beige",variable=themes,command=change_theme)
themes_menu.add_radiobutton(label="Cobalt Blue",variable=themes,command=change_theme)
themes_menu.add_radiobutton(label="Greygarious",variable=themes,command=change_theme)
themes_menu.add_radiobutton(label="Night Mode",variable=themes,command=change_theme)
view_menu.add_cascade(label='theme',menu=themes_menu)

about_menu=Menu(menu_bar,tearoff=0)
about_menu.add_command(label='about',command=show_about)
about_menu.add_command(label='help',command=show_help)
menu_bar.add_cascade(label="File",menu=file_menu)
menu_bar.add_cascade(label="Edit",menu=edit_menu)
menu_bar.add_cascade(label="View",menu=view_menu)
menu_bar.add_cascade(label="About",menu=about_menu)
root.config(menu=menu_bar)

shortcut_bar=Frame(root,background='light sea green',height=25)
shortcut_bar.pack(expand='no',fill='x')
line_no_bar = Text(root, width=4, padx=3, takefocus=0,
border=0,
background='khaki', state='disabled', wrap='none')
line_no_bar.pack(side='left', fill='y')
content_text=Text(root,wrap='word',undo=1)
content_text.focus_set()
content_text.pack(fill='both',expand='yes')
scroll_bar=Scrollbar(content_text)
content_text.configure(yscrollcommand=scroll_bar.set)
scroll_bar.configure(command=content_text.yview)
scroll_bar.pack(fill='y',side='right')
cursor_info=Label(content_text,text='Line : 1 | column : 1')
cursor_info.pack(expand='no',fill='none',side='right',anchor='se')

image=('new_file', 'open_file', 'save', 'cut', 'copy', 'paste',
'undo', 'redo', 'find_text')
icon_image=()
for i in range(0,len(image)):
     icon_image=Image.open("icons/{}.png".format(image[i]))
     icon=ImageTk.PhotoImage(icon_image)
     cmd=eval(image[i])
     tool_bar=Button(shortcut_bar,image=icon,command=cmd)
     tool_bar.image = icon
     tool_bar.pack(side='left')

popup_menu = Menu(content_text)
for i in ('cut', 'copy', 'paste', 'undo', 'redo'):
 cmd = eval(i)
 popup_menu.add_command(label=i, compound='left', command=cmd)
popup_menu.add_separator()
popup_menu.add_command(label='Select All', underline=7,
command=select_all)
 
content_text.bind('<Button-3>', show_popup_menu)    
content_text.bind('<Control-Y>',redo)
content_text.bind('<Control-y>',redo)
content_text.bind('<Control-f>',find_text)
content_text.bind('<Control-F>',find_text)
content_text.bind('<Control-A>',select_all)
content_text.bind('<Control-a>',select_all)
content_text.bind('<Control-o>',open_file)
content_text.bind('<Control-O>',open_file)
content_text.bind('<Shift-Control-S>',saveas)
content_text.bind('<Shift-Control-s>',saveas)
content_text.bind('<Control-S>',save)
content_text.bind('<Control-s>',save)
content_text.bind('<Control-N>',new_file)
content_text.bind('<Control-n>',new_file)
content_text.bind('<Any-KeyPress>',on_content_changed)
content_text.tag_configure('active_line',background='ivory2')
root.mainloop()
