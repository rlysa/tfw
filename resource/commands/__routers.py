from .start import router as start_router
from .registration import router as registration_router
from .admin_commands.main_admin import router as admin_main_router
from .admin_commands.look_interns_info import router as look_interns_info_router
from .admin_commands.look_groups_info import router as look_groups_info_router
# from .intern_commands.view_the_task_list import router as view_the_task_list_router
from .intern_commands.view_task_description import router as view_task_description_router
from .intern_commands.view_group_composition import router as view_group_composition_router
from .intern_commands.view_check_my_info import router as view_check_my_info_router
from .intern_commands.action_selection_menu import router as action_selection_menu_router
from .intern_commands.change_my_info import router as change_my_info_router
from .admin_commands.create_task import router as create_task_router
from .admin_commands.create_group import router as create_group_router
# from .admin_commands.accept_new_user import router as accept_new_user_router
from .admin_commands.change_profile import router as change_profile_router
