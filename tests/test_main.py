import pygame
import sys
from unittest import mock
import importlib
import os


# Import after patching
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
main = importlib.import_module("main")

def test_generate_white_noise_returns_sound():
    sound = main.generate_white_noise(volume=0.1)
    assert hasattr(sound, "play") or isinstance(sound, mock.Mock)

def test_update_scene_menu(monkeypatch):
    called = {}
    def fake_menu(surface, buttons, offset):
        called['menu'] = (surface, buttons, offset)
    monkeypatch.setattr(main, "menu", fake_menu)
    state = {'is_menu': True, 'level': 0}
    main.update_scene(state, buttons="btns", offset_x_y=(0, 0))
    assert 'menu' in called

def test_update_scene_scene(monkeypatch):
    called = {}
    def fake_scene(surface, content):
        called['scene'] = (surface, content)
    monkeypatch.setattr(main, "scene", fake_scene)
    monkeypatch.setattr(main, "content", ["dialog1", "dialog2"])
    state = {'is_menu': False, 'level': 1}
    main.update_scene(state, buttons="btns", offset_x_y=(0, 0))
    assert 'scene' in called
    assert called['scene'][1] == "dialog2"

def test_update_scene_scene_indexerror(monkeypatch):
    called = {}
    def fake_scene(surface, content):
        called['scene'] = (surface, content)
        raise IndexError
    monkeypatch.setattr(main, "scene", fake_scene)
    monkeypatch.setattr(main, "content", ["dialog1"])
    state = {'is_menu': False, 'level': 5}
    # Should not raise
    main.update_scene(state, buttons="btns", offset_x_y=(0, 0))

def test_main_quit(monkeypatch):
    # Patch dependencies
    monkeypatch.setattr(main, "create_menu_buttons", lambda state: "buttons")
    monkeypatch.setattr(main, "generate_white_noise", lambda volume: mock.Mock(play=lambda loops: None))
    # Simulate QUIT event
    fake_event = mock.Mock()
    fake_event.type = pygame.QUIT
    monkeypatch.setattr(main.pygame, "event", mock.Mock(get=lambda: [fake_event]))
    monkeypatch.setattr(main.pygame, "quit", lambda: None)
    # Patch update_scene to avoid side effects
    monkeypatch.setattr(main, "update_scene", lambda *a, **kw: None)
    # Patch display and clock
    main.screen = mock.Mock()
    main.screen.get_size.return_value = (800, 600)
    main.screen.blit = lambda *a, **kw: None
    main.screen.fill = lambda *a, **kw: None
    main.game_surface = mock.Mock()
    main.game_surface.fill = lambda *a, **kw: None
    main.clock = mock.Mock()
    main.clock.tick = lambda x: None
    main.pygame.display.flip = lambda: None
    # Should exit main loop and return
    assert main.main() is None