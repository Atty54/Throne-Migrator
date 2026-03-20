import tkinter as tk
from tkinter import filedialog, messagebox
import sqlite3

def select_old_db():
    filepath = filedialog.askopenfilename(
        title="Select Old Throne DB",
        filetypes=(("SQLite Database", "*.db"), ("All Files", "*.*"))
    )
    if filepath:
        entry_old_db.delete(0, tk.END)
        entry_old_db.insert(0, filepath)

def select_new_db():
    filepath = filedialog.askopenfilename(
        title="Select New Throne DB",
        filetypes=(("SQLite Database", "*.db"), ("All Files", "*.*"))
    )
    if filepath:
        entry_new_db.delete(0, tk.END)
        entry_new_db.insert(0, filepath)

def run_migration():
    old_db_path = entry_old_db.get()
    new_db_path = entry_new_db.get()

    if not old_db_path or not new_db_path:
        messagebox.showwarning("Warning", "Please select both paths!")
        return

    # Подготавливаем пути: SQLite требует прямые слеши
    old_db_clean = old_db_path.replace('\\', '/')
    
    # Формируем SQL-запрос
    sql_script = f"""
    ATTACH DATABASE '{old_db_clean}' AS old_db;
    
    BEGIN TRANSACTION;

    DELETE FROM entity_ids;
    DELETE FROM groups;
    DELETE FROM groups_order;
    DELETE FROM profiles;
    DELETE FROM route_profiles;
    DELETE FROM route_rules;
    DELETE FROM settings;

    INSERT INTO entity_ids SELECT * FROM old_db.entity_ids;
    INSERT INTO groups_order SELECT * FROM old_db.groups_order;
    INSERT INTO route_profiles SELECT * FROM old_db.route_profiles;
    INSERT INTO route_rules SELECT * FROM old_db.route_rules;
    INSERT INTO settings SELECT * FROM old_db.settings;

    INSERT INTO groups (
        id, archive, skip_auto_update, name, url, info, sub_last_update, 
        front_proxy_id, landing_proxy_id, column_width_json, profiles_json, 
        scroll_last_profile, auto_clear_unavailable, test_sort_by, 
        traffic_sort_by, test_items_to_show, created_at, updated_at
    )
    SELECT 
        id, archive, skip_auto_update, name, url, info, sub_last_update, 
        front_proxy_id, landing_proxy_id, column_width_json, profiles_json, 
        scroll_last_profile, auto_clear_unavailable, test_sort_by, 
        0, test_items_to_show, created_at, updated_at
    FROM old_db.groups;

    INSERT INTO profiles (
        id, type, name, gid, latency, dl_speed, ul_speed, test_country, 
        ip_out, outbound_json, traffic_dl, traffic_up, created_at, updated_at
    )
    SELECT 
        id, type, name, gid, latency, dl_speed, ul_speed, test_country, 
        ip_out, outbound_json, 0, 0, created_at, updated_at
    FROM old_db.profiles;

    COMMIT;
    DETACH DATABASE old_db;
    """

    try:
        # Подключаемся к НОВОЙ базе и выполняем скрипт, который сам подтянет старую
        conn = sqlite3.connect(new_db_path)
        cursor = conn.cursor()
        cursor.executescript(sql_script)
        conn.close()
        
        messagebox.showinfo("Success", "Complete")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred:\n{str(e)}")

# --- Настройка графического интерфейса ---
root = tk.Tk()
root.title("Throne DB Migrator by github.com/Atty54")
root.geometry("500x180")
root.resizable(False, False)

# Блок для старой БД
tk.Label(root, text="Path to old Throne DB:").pack(anchor="w", padx=10, pady=(10, 0))
frame_old = tk.Frame(root)
frame_old.pack(fill="x", padx=10)
entry_old_db = tk.Entry(frame_old)
entry_old_db.pack(side="left", fill="x", expand=True)
tk.Button(frame_old, text="Browse", command=select_old_db).pack(side="right", padx=(5, 0))

# Блок для новой БД
tk.Label(root, text="Path to new Throne DB:").pack(anchor="w", padx=10, pady=(10, 0))
frame_new = tk.Frame(root)
frame_new.pack(fill="x", padx=10)
entry_new_db = tk.Entry(frame_new)
entry_new_db.pack(side="left", fill="x", expand=True)
tk.Button(frame_new, text="Browse", command=select_new_db).pack(side="right", padx=(5, 0))

# Кнопка GO с принудительной высотой
btn_go = tk.Button(
    root, 
    text="GO", 
    command=run_migration, 
    bg="#4CAF50", 
    fg="white", 
    font=("Arial", 10, "bold"),
    height=2,       # Высота в СТРОКАХ текста (в Linux это спасет от "полоски")
    width=15,       # Ширина в СИМВОЛАХ
    cursor="hand2"
)

# Используем pady для внешнего отступа от полей ввода
btn_go.pack(pady=15)

root.mainloop()
