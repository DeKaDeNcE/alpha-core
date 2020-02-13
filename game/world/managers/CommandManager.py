from struct import pack

from game.world.managers.GridManager import GridManager
from network.packet.PacketWriter import PacketWriter, OpCode
from game.world.managers.ChatManager import ChatManager


class CommandManager(object):

    @staticmethod
    def handle_command(world_session, command_msg):
        terminator_index = command_msg.find(' ') if ' ' in command_msg else len(command_msg)

        command = command_msg[1:terminator_index].strip()
        args = command_msg[terminator_index:].strip()
        command_func = None

        if command in PLAYER_COMMAND_DEFINITIONS:
            command_func = PLAYER_COMMAND_DEFINITIONS.get(command)
        elif command in GM_COMMAND_DEFINITIONS and world_session.player_mgr.is_gm:
            command_func = GM_COMMAND_DEFINITIONS.get(command)
        else:
            ChatManager.send_system_message(world_session, 'Command not found.')

        if command_func and command_func(world_session, args) != 0:
            ChatManager.send_system_message(world_session, 'Wrong arguments for <%s> command.' % command)

    @staticmethod
    def speed(world_session, args):
        try:
            speed = float(args)
            world_session.player_mgr.change_speed(speed)

            return 0
        except ValueError:
            return -1

    @staticmethod
    def gps(world_session, args):
        ChatManager.send_system_message(world_session, 'Map: %u, Zone: %u, X: %f, Y: %f, Z: %f, O: %f' % (
            world_session.player_mgr.map_,
            world_session.player_mgr.zone,
            world_session.player_mgr.location.x,
            world_session.player_mgr.location.y,
            world_session.player_mgr.location.z,
            world_session.player_mgr.location.o
        ))

        return 0


PLAYER_COMMAND_DEFINITIONS = {

}

GM_COMMAND_DEFINITIONS = {
    'speed': CommandManager.speed,
    'gps': CommandManager.gps
}