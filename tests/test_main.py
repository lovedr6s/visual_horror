import pytest
import pygame
import sys
from unittest import mock
import importlib
import os

# Patch pygame modules that require a display/audio device for headless testing
@pytest.fixture(autouse=True)
def patch_pygame(monkeypatch):
    monkeypatch.setattr(pygame, "init", lambda: None)
    monkeypatch.setattr(pygame.mixer, "init", lambda *a, **kw: None)
    monkeypatch.setattr(pygame.display, "set_icon", lambda icon: None)
    monkeypatch.setattr(pygame.display, "set_caption", lambda caption: None)
    monkeypatch.setattr(pygame.display, "set_mode", lambda *a, **kw: mock.Mock())
    monkeypatch.setattr(pygame.time, "Clock", lambda: mock.Mock())
    monkeypatch.setattr(pygame.image, "load", lambda path: mock.Mock())
    monkeypatch.setattr(pygame.sndarray, "make_sound", lambda arr: mock.Mock(spec=pygame.mixer.Sound))
    monkeypatch.setattr(pygame, "QUIT", 12)
    monkeypatch.setattr(pygame, "MOUSEBUTTONDOWN", 5)
    monkeypatch.setattr(pygame, "KEYDOWN", 2)
    monkeypatch.setattr(pygame, "K_SPACE", 32)
    monkeypatch.setattr(pygame, "K_RETURN", 13)
    monkeypatch.setattr(pygame, "K_ESCAPE", 27)
    monkeypatch.setattr(pygame, "RESIZABLE", 0)
    monkeypatch.setattr(pygame, "display", mock.Mock())
    monkeypatch.setattr(pygame, "event", mock.Mock())
    monkeypatch.setattr(pygame, "mixer", mock.Mock())
    monkeypatch.setattr(pygame, "Surface", lambda *a, **kw: mock.Mock())
    monkeypatch.setattr(pygame, "time", mock.Mock())
    monkeypatch.setattr(pygame, "image", mock.Mock())
    monkeypatch.setattr(pygame, "sndarray", mock.Mock())
    monkeypatch.setattr(pygame, "mixer", mock.Mock())
    monkeypatch.setattr(pygame, "display", mock.Mock())
    monkeypatch.setattr(pygame, "quit", lambda: None)

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