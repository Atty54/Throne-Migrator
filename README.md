# Throne-Migrator

Migrating from DB Beta to DB Release in Throne

🇷🇺 Русская версия: [README.ru.md](README.ru.md)

---

## Description

This program is designed for migrating database format from **Throne Beta versions** to the **Throne Release version**.

---

## How to use

1. Run the **release version of Throne** once.
2. Close it completely (make sure it is not running in the system tray).
3. Launch **Throne-Migrator**.
4. Click **Browse** next to:
   - **Path to old Throne DB** → select `throne.db` from the Beta version
   - **Path to new Throne DB** → select `throne.db` from the Release version
5. Make sure both fields are filled.
6. Click **Go**.
7. Wait until the program finishes (you will see `Complete`).
8. Close the migrator.
9. Launch the **release version of Throne** and verify your data.

---

## Notes

- Make sure both database files are accessible.
- It is recommended to create backups before migration.

---

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
