import flet as ft
import pandas as pd
import os


def get_file_info(path):
    try:
        stat = os.stat(path)
        return {
            "Path": path,
            "Creation_date": stat.st_ctime,
            "Size (kB)": stat.st_size,
            "Owner": stat.st_uid,
        }
    except Exception as e:
        print(f"Error getting info for {path}: {e}")
        return None


def get_all_files(path, filters={}):
    """" Iterate over all files in path. """
    file_infos = []
    for dirpath, dirnames, filenames in os.walk(path):
        for filename in [f for f in filenames]:
            file_info = get_file_info(os.path.join(dirpath, filename))
            if file_info:
                file_infos.append(file_info)
    df_files = pd.DataFrame(file_infos)
    return df_files


def on_click(page):
    """ On button press. """

    def pick_files_result(e: ft.FilePickerResultEvent):
        global path_search
        path_search = e.path
        print(e.path)

    path_picker = ft.FilePicker(on_result=pick_files_result)

    page.overlay.append(path_picker)
    page.update()
    path_picker.get_directory_path()


def search_path(page: ft.Page):
    global path_search
    if path_search:
        df = get_all_files(path_search)
        if not df.empty:

            lv = ft.ListView(expand=1, spacing=10, padding=20, horizontal=True)

            # For further information: https://flet.dev/docs/controls/datatable
            df_view = ft.DataTable(
                bgcolor="lightblue",
                border=ft.border.all(2, "red"),
                columns=[ft.DataColumn(ft.Text(t)) for t in df.columns],
                rows=[ft.DataRow(cells=[ft.DataCell(ft.Text(str(v))) for v in row]) for i, row in df.iterrows()]
            )

            # Create both vertical and horizontal scrollbars:
            column = ft.Column([df_view], scroll=ft.ScrollMode.ALWAYS)

            # todo: make the df head freeze.

            lv.controls.append(column)
            page.add(lv)

            page.add(df_view)
            page.update()


def build_filter_ui(page):
    # Add UI elements for filters (e.g., checkboxes, dropdown menus)
    # Update the get_all_files function based on user selections
    pass


def main(page: ft.Page):
    page.title = "File Explorer"  # Set title after creating the page
    button_dir_pick = ft.ElevatedButton("Choose Path", on_click=lambda ev: on_click(page))
    page.add(button_dir_pick)
    button_search = ft.ElevatedButton("Search", on_click=lambda ev: search_path(page))
    page.add(button_search)

    build_filter_ui(page)

path_search = ''
ft.app(target=main)
