from django.conf.urls import url

from . import views

# Automatically add these URLs when the application is installed
autodiscover = True

urlpatterns = [
    url(r"^execute/$", views.TaskReport.as_view(), name="execute"),
    url(
        r"^execute/logfrepple/(.+)/$",
        views.logfile,
        name="execute_view_log",
    ),
    url(
        r"^execute/launch/(.+)/$",
        views.LaunchTask,
        name="execute_launch",
    ),
    url(
        r"^execute/cancel/(.+)/$",
        views.CancelTask,
        name="execute_cancel",
    ),
    url(
        r"^execute/logdownload/(.+)/$",
        views.DownloadLogFile,
        name="execute_download_log",
    ),
    url(r"^execute/api/(.+)/$", views.APITask, name="execute_api"),
    url(
        r"^execute/uploadtofolder/(.+)/$",
        views.FileManager.uploadFiletoFolder,
        name="copy_file_to_folder",
    ),
    url(
        r"^execute/downloadfromfolder/(.+)/(.+)/$",
        views.FileManager.downloadFilefromFolder,
        name="download_file_from_folder",
    ),
    url(
        r"^execute/downloadfromfolder/(.+)/$",
        views.FileManager.downloadFilefromFolder,
        name="download_all_files_from_folder",
    ),
    url(
        r"^execute/deletefromfolder/(.+)/(.+)/$",
        views.FileManager.deleteFilefromFolder,
        name="delete_file_from_folder",
    ),
    url(
        r"^execute/scheduletasks/$",
        views.scheduletasks,
        name="scheduletasks",
    ),
]
