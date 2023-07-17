# Copyright 2022 NXP
# SPDX-License-Identifier: MIT
# The auto-generated can only be used on NXP devices

import SDL
import utime as time
import usys as sys
import lvgl as lv
import lodepng as png
import ustruct

lv.init()
SDL.init(w=480,h=320)

# Register SDL display driver.
disp_buf1 = lv.disp_draw_buf_t()
buf1_1 = bytearray(480*10)
disp_buf1.init(buf1_1, None, len(buf1_1)//4)
disp_drv = lv.disp_drv_t()
disp_drv.init()
disp_drv.draw_buf = disp_buf1
disp_drv.flush_cb = SDL.monitor_flush
disp_drv.hor_res = 480
disp_drv.ver_res = 320
disp_drv.register()

# Regsiter SDL mouse driver
indev_drv = lv.indev_drv_t()
indev_drv.init() 
indev_drv.type = lv.INDEV_TYPE.POINTER
indev_drv.read_cb = SDL.mouse_read
indev_drv.register()

# Below: Taken from https://github.com/lvgl/lv_binding_micropython/blob/master/driver/js/imagetools.py#L22-L94

COLOR_SIZE = lv.color_t.__SIZE__
COLOR_IS_SWAPPED = hasattr(lv.color_t().ch,'green_h')

class lodepng_error(RuntimeError):
    def __init__(self, err):
        if type(err) is int:
            super().__init__(png.error_text(err))
        else:
            super().__init__(err)

# Parse PNG file header
# Taken from https://github.com/shibukawa/imagesize_py/blob/ffef30c1a4715c5acf90e8945ceb77f4a2ed2d45/imagesize.py#L63-L85

def get_png_info(decoder, src, header):
    # Only handle variable image types

    if lv.img.src_get_type(src) != lv.img.SRC.VARIABLE:
        return lv.RES.INV

    data = lv.img_dsc_t.__cast__(src).data
    if data == None:
        return lv.RES.INV

    png_header = bytes(data.__dereference__(24))

    if png_header.startswith(b'\211PNG\r\n\032\n'):
        if png_header[12:16] == b'IHDR':
            start = 16
        # Maybe this is for an older PNG version.
        else:
            start = 8
        try:
            width, height = ustruct.unpack(">LL", png_header[start:start+8])
        except ustruct.error:
            return lv.RES.INV
    else:
        return lv.RES.INV

    header.always_zero = 0
    header.w = width
    header.h = height
    header.cf = lv.img.CF.TRUE_COLOR_ALPHA

    return lv.RES.OK

def convert_rgba8888_to_bgra8888(img_view):
    for i in range(0, len(img_view), lv.color_t.__SIZE__):
        ch = lv.color_t.__cast__(img_view[i:i]).ch
        ch.red, ch.blue = ch.blue, ch.red

# Read and parse PNG file

def open_png(decoder, dsc):
    img_dsc = lv.img_dsc_t.__cast__(dsc.src)
    png_data = img_dsc.data
    png_size = img_dsc.data_size
    png_decoded = png.C_Pointer()
    png_width = png.C_Pointer()
    png_height = png.C_Pointer()
    error = png.decode32(png_decoded, png_width, png_height, png_data, png_size)
    if error:
        raise lodepng_error(error)
    img_size = png_width.int_val * png_height.int_val * 4
    img_data = png_decoded.ptr_val
    img_view = img_data.__dereference__(img_size)

    if COLOR_SIZE == 4:
        convert_rgba8888_to_bgra8888(img_view)
    else:
        raise lodepng_error("Error: Color mode not supported yet!")

    dsc.img_data = img_data
    return lv.RES.OK

# Above: Taken from https://github.com/lvgl/lv_binding_micropython/blob/master/driver/js/imagetools.py#L22-L94

decoder = lv.img.decoder_create()
decoder.info_cb = get_png_info
decoder.open_cb = open_png

def anim_x_cb(obj, v):
    obj.set_x(v)

def anim_y_cb(obj, v):
    obj.set_y(v)

def ta_event_cb(e,kb):
    code = e.get_code()
    ta = e.get_target()
    if code == lv.EVENT.FOCUSED:
        kb.set_textarea(ta)
        kb.move_foreground()
        kb.clear_flag(lv.obj.FLAG.HIDDEN)

    if code == lv.EVENT.DEFOCUSED:
        kb.set_textarea(None)
        kb.move_background()
        kb.add_flag(lv.obj.FLAG.HIDDEN)



# create screen
screen = lv.obj()
screen.set_scrollbar_mode(lv.SCROLLBAR_MODE.OFF)
# create style style_screen_main_main_default
style_screen_main_main_default = lv.style_t()
style_screen_main_main_default.init()
style_screen_main_main_default.set_bg_color(lv.color_make(0xff,0xff,0xff))
style_screen_main_main_default.set_bg_opa(0)

# add style for screen
screen.add_style(style_screen_main_main_default, lv.PART.MAIN|lv.STATE.DEFAULT)


# create screen_img_8
screen_img_8 = lv.img(screen)
screen_img_8.set_pos(int(345),int(219))
screen_img_8.set_size(45,40)
screen_img_8.set_scrollbar_mode(lv.SCROLLBAR_MODE.OFF)
screen_img_8.add_flag(lv.obj.FLAG.CLICKABLE)
try:
    with open('C:\\NXP\\GUI-Guider-Projects\\dadishu_spi\\generated\\mPythonImages\\mp1699735897.png','rb') as f:
        screen_img_8_img_data = f.read()
except:
    print('Could not open C:\\NXP\\GUI-Guider-Projects\\dadishu_spi\\generated\\mPythonImages\\mp1699735897.png')
    sys.exit()

screen_img_8_img = lv.img_dsc_t({
  'data_size': len(screen_img_8_img_data),
  'header': {'always_zero': 0, 'w': 45, 'h': 40, 'cf': lv.img.CF.TRUE_COLOR_ALPHA},
  'data': screen_img_8_img_data
})

screen_img_8.set_src(screen_img_8_img)
screen_img_8.set_pivot(50,50)
screen_img_8.set_angle(0)
# create style style_screen_img_8_main_main_default
style_screen_img_8_main_main_default = lv.style_t()
style_screen_img_8_main_main_default.init()
style_screen_img_8_main_main_default.set_img_recolor(lv.color_make(0xff,0xff,0xff))
style_screen_img_8_main_main_default.set_img_recolor_opa(0)
style_screen_img_8_main_main_default.set_img_opa(255)

# add style for screen_img_8
screen_img_8.add_style(style_screen_img_8_main_main_default, lv.PART.MAIN|lv.STATE.DEFAULT)


# create screen_img_7
screen_img_7 = lv.img(screen)
screen_img_7.set_pos(int(218),int(219))
screen_img_7.set_size(45,40)
screen_img_7.set_scrollbar_mode(lv.SCROLLBAR_MODE.OFF)
screen_img_7.add_flag(lv.obj.FLAG.CLICKABLE)
try:
    with open('C:\\NXP\\GUI-Guider-Projects\\dadishu_spi\\generated\\mPythonImages\\mp1699735897.png','rb') as f:
        screen_img_7_img_data = f.read()
except:
    print('Could not open C:\\NXP\\GUI-Guider-Projects\\dadishu_spi\\generated\\mPythonImages\\mp1699735897.png')
    sys.exit()

screen_img_7_img = lv.img_dsc_t({
  'data_size': len(screen_img_7_img_data),
  'header': {'always_zero': 0, 'w': 45, 'h': 40, 'cf': lv.img.CF.TRUE_COLOR_ALPHA},
  'data': screen_img_7_img_data
})

screen_img_7.set_src(screen_img_7_img)
screen_img_7.set_pivot(50,50)
screen_img_7.set_angle(0)
# create style style_screen_img_7_main_main_default
style_screen_img_7_main_main_default = lv.style_t()
style_screen_img_7_main_main_default.init()
style_screen_img_7_main_main_default.set_img_recolor(lv.color_make(0xff,0xff,0xff))
style_screen_img_7_main_main_default.set_img_recolor_opa(0)
style_screen_img_7_main_main_default.set_img_opa(255)

# add style for screen_img_7
screen_img_7.add_style(style_screen_img_7_main_main_default, lv.PART.MAIN|lv.STATE.DEFAULT)


# create screen_img_6
screen_img_6 = lv.img(screen)
screen_img_6.set_pos(int(92),int(219))
screen_img_6.set_size(45,40)
screen_img_6.set_scrollbar_mode(lv.SCROLLBAR_MODE.OFF)
screen_img_6.add_flag(lv.obj.FLAG.CLICKABLE)
try:
    with open('C:\\NXP\\GUI-Guider-Projects\\dadishu_spi\\generated\\mPythonImages\\mp1699735897.png','rb') as f:
        screen_img_6_img_data = f.read()
except:
    print('Could not open C:\\NXP\\GUI-Guider-Projects\\dadishu_spi\\generated\\mPythonImages\\mp1699735897.png')
    sys.exit()

screen_img_6_img = lv.img_dsc_t({
  'data_size': len(screen_img_6_img_data),
  'header': {'always_zero': 0, 'w': 45, 'h': 40, 'cf': lv.img.CF.TRUE_COLOR_ALPHA},
  'data': screen_img_6_img_data
})

screen_img_6.set_src(screen_img_6_img)
screen_img_6.set_pivot(50,50)
screen_img_6.set_angle(0)
# create style style_screen_img_6_main_main_default
style_screen_img_6_main_main_default = lv.style_t()
style_screen_img_6_main_main_default.init()
style_screen_img_6_main_main_default.set_img_recolor(lv.color_make(0xff,0xff,0xff))
style_screen_img_6_main_main_default.set_img_recolor_opa(0)
style_screen_img_6_main_main_default.set_img_opa(255)

# add style for screen_img_6
screen_img_6.add_style(style_screen_img_6_main_main_default, lv.PART.MAIN|lv.STATE.DEFAULT)


# create screen_img_5
screen_img_5 = lv.img(screen)
screen_img_5.set_pos(int(345),int(143))
screen_img_5.set_size(45,40)
screen_img_5.set_scrollbar_mode(lv.SCROLLBAR_MODE.OFF)
screen_img_5.add_flag(lv.obj.FLAG.CLICKABLE)
try:
    with open('C:\\NXP\\GUI-Guider-Projects\\dadishu_spi\\generated\\mPythonImages\\mp1699735897.png','rb') as f:
        screen_img_5_img_data = f.read()
except:
    print('Could not open C:\\NXP\\GUI-Guider-Projects\\dadishu_spi\\generated\\mPythonImages\\mp1699735897.png')
    sys.exit()

screen_img_5_img = lv.img_dsc_t({
  'data_size': len(screen_img_5_img_data),
  'header': {'always_zero': 0, 'w': 45, 'h': 40, 'cf': lv.img.CF.TRUE_COLOR_ALPHA},
  'data': screen_img_5_img_data
})

screen_img_5.set_src(screen_img_5_img)
screen_img_5.set_pivot(50,50)
screen_img_5.set_angle(0)
# create style style_screen_img_5_main_main_default
style_screen_img_5_main_main_default = lv.style_t()
style_screen_img_5_main_main_default.init()
style_screen_img_5_main_main_default.set_img_recolor(lv.color_make(0xff,0xff,0xff))
style_screen_img_5_main_main_default.set_img_recolor_opa(0)
style_screen_img_5_main_main_default.set_img_opa(255)

# add style for screen_img_5
screen_img_5.add_style(style_screen_img_5_main_main_default, lv.PART.MAIN|lv.STATE.DEFAULT)


# create screen_img_4
screen_img_4 = lv.img(screen)
screen_img_4.set_pos(int(218),int(143))
screen_img_4.set_size(45,40)
screen_img_4.set_scrollbar_mode(lv.SCROLLBAR_MODE.OFF)
screen_img_4.add_flag(lv.obj.FLAG.CLICKABLE)
try:
    with open('C:\\NXP\\GUI-Guider-Projects\\dadishu_spi\\generated\\mPythonImages\\mp1699735897.png','rb') as f:
        screen_img_4_img_data = f.read()
except:
    print('Could not open C:\\NXP\\GUI-Guider-Projects\\dadishu_spi\\generated\\mPythonImages\\mp1699735897.png')
    sys.exit()

screen_img_4_img = lv.img_dsc_t({
  'data_size': len(screen_img_4_img_data),
  'header': {'always_zero': 0, 'w': 45, 'h': 40, 'cf': lv.img.CF.TRUE_COLOR_ALPHA},
  'data': screen_img_4_img_data
})

screen_img_4.set_src(screen_img_4_img)
screen_img_4.set_pivot(50,50)
screen_img_4.set_angle(0)
# create style style_screen_img_4_main_main_default
style_screen_img_4_main_main_default = lv.style_t()
style_screen_img_4_main_main_default.init()
style_screen_img_4_main_main_default.set_img_recolor(lv.color_make(0xff,0xff,0xff))
style_screen_img_4_main_main_default.set_img_recolor_opa(0)
style_screen_img_4_main_main_default.set_img_opa(255)

# add style for screen_img_4
screen_img_4.add_style(style_screen_img_4_main_main_default, lv.PART.MAIN|lv.STATE.DEFAULT)


# create screen_img_1
screen_img_1 = lv.img(screen)
screen_img_1.set_pos(int(0),int(0))
screen_img_1.set_size(480,320)
screen_img_1.set_scrollbar_mode(lv.SCROLLBAR_MODE.OFF)
screen_img_1.add_flag(lv.obj.FLAG.CLICKABLE)
try:
    with open('C:\\NXP\\GUI-Guider-Projects\\dadishu_spi\\generated\\mPythonImages\\mp-1374753916.png','rb') as f:
        screen_img_1_img_data = f.read()
except:
    print('Could not open C:\\NXP\\GUI-Guider-Projects\\dadishu_spi\\generated\\mPythonImages\\mp-1374753916.png')
    sys.exit()

screen_img_1_img = lv.img_dsc_t({
  'data_size': len(screen_img_1_img_data),
  'header': {'always_zero': 0, 'w': 480, 'h': 320, 'cf': lv.img.CF.TRUE_COLOR_ALPHA},
  'data': screen_img_1_img_data
})

screen_img_1.set_src(screen_img_1_img)
screen_img_1.set_pivot(50,50)
screen_img_1.set_angle(0)
# create style style_screen_img_1_main_main_default
style_screen_img_1_main_main_default = lv.style_t()
style_screen_img_1_main_main_default.init()
style_screen_img_1_main_main_default.set_img_recolor(lv.color_make(0xff,0xff,0xff))
style_screen_img_1_main_main_default.set_img_recolor_opa(0)
style_screen_img_1_main_main_default.set_img_opa(255)

# add style for screen_img_1
screen_img_1.add_style(style_screen_img_1_main_main_default, lv.PART.MAIN|lv.STATE.DEFAULT)


# create screen_img_3
screen_img_3 = lv.img(screen)
screen_img_3.set_pos(int(218),int(219))
screen_img_3.set_size(45,40)
screen_img_3.set_scrollbar_mode(lv.SCROLLBAR_MODE.OFF)
screen_img_3.add_flag(lv.obj.FLAG.CLICKABLE)
try:
    with open('C:\\NXP\\GUI-Guider-Projects\\dadishu_spi\\generated\\mPythonImages\\mp1302428205.png','rb') as f:
        screen_img_3_img_data = f.read()
except:
    print('Could not open C:\\NXP\\GUI-Guider-Projects\\dadishu_spi\\generated\\mPythonImages\\mp1302428205.png')
    sys.exit()

screen_img_3_img = lv.img_dsc_t({
  'data_size': len(screen_img_3_img_data),
  'header': {'always_zero': 0, 'w': 45, 'h': 40, 'cf': lv.img.CF.TRUE_COLOR_ALPHA},
  'data': screen_img_3_img_data
})

screen_img_3.set_src(screen_img_3_img)
screen_img_3.set_pivot(50,50)
screen_img_3.set_angle(0)
# create style style_screen_img_3_main_main_default
style_screen_img_3_main_main_default = lv.style_t()
style_screen_img_3_main_main_default.init()
style_screen_img_3_main_main_default.set_img_recolor(lv.color_make(0xff,0xff,0xff))
style_screen_img_3_main_main_default.set_img_recolor_opa(0)
style_screen_img_3_main_main_default.set_img_opa(255)

# add style for screen_img_3
screen_img_3.add_style(style_screen_img_3_main_main_default, lv.PART.MAIN|lv.STATE.DEFAULT)


# create screen_img_2
screen_img_2 = lv.img(screen)
screen_img_2.set_pos(int(92),int(143))
screen_img_2.set_size(45,40)
screen_img_2.set_scrollbar_mode(lv.SCROLLBAR_MODE.OFF)
screen_img_2.add_flag(lv.obj.FLAG.CLICKABLE)
try:
    with open('C:\\NXP\\GUI-Guider-Projects\\dadishu_spi\\generated\\mPythonImages\\mp1699735897.png','rb') as f:
        screen_img_2_img_data = f.read()
except:
    print('Could not open C:\\NXP\\GUI-Guider-Projects\\dadishu_spi\\generated\\mPythonImages\\mp1699735897.png')
    sys.exit()

screen_img_2_img = lv.img_dsc_t({
  'data_size': len(screen_img_2_img_data),
  'header': {'always_zero': 0, 'w': 45, 'h': 40, 'cf': lv.img.CF.TRUE_COLOR_ALPHA},
  'data': screen_img_2_img_data
})

screen_img_2.set_src(screen_img_2_img)
screen_img_2.set_pivot(50,50)
screen_img_2.set_angle(0)
# create style style_screen_img_2_main_main_default
style_screen_img_2_main_main_default = lv.style_t()
style_screen_img_2_main_main_default.init()
style_screen_img_2_main_main_default.set_img_recolor(lv.color_make(0xff,0xff,0xff))
style_screen_img_2_main_main_default.set_img_recolor_opa(0)
style_screen_img_2_main_main_default.set_img_opa(255)

# add style for screen_img_2
screen_img_2.add_style(style_screen_img_2_main_main_default, lv.PART.MAIN|lv.STATE.DEFAULT)


# create screen_btn_1
screen_btn_1 = lv.btn(screen)
screen_btn_1.set_pos(int(325),int(6))
screen_btn_1.set_size(65,35)
screen_btn_1.set_scrollbar_mode(lv.SCROLLBAR_MODE.OFF)
screen_btn_1_label = lv.label(screen_btn_1)
screen_btn_1_label.set_text("Start")
screen_btn_1.set_style_pad_all(0, lv.STATE.DEFAULT)
screen_btn_1_label.align(lv.ALIGN.CENTER,0,0)
# create style style_screen_btn_1_main_main_default
style_screen_btn_1_main_main_default = lv.style_t()
style_screen_btn_1_main_main_default.init()
style_screen_btn_1_main_main_default.set_radius(5)
style_screen_btn_1_main_main_default.set_bg_color(lv.color_make(0x21,0x95,0xf6))
style_screen_btn_1_main_main_default.set_bg_grad_color(lv.color_make(0x21,0x95,0xf6))
style_screen_btn_1_main_main_default.set_bg_grad_dir(lv.GRAD_DIR.NONE)
style_screen_btn_1_main_main_default.set_bg_opa(255)
style_screen_btn_1_main_main_default.set_border_color(lv.color_make(0x21,0x95,0xf6))
style_screen_btn_1_main_main_default.set_border_width(0)
style_screen_btn_1_main_main_default.set_border_opa(255)
style_screen_btn_1_main_main_default.set_text_color(lv.color_make(0xff,0xff,0xff))
try:
    style_screen_btn_1_main_main_default.set_text_font(lv.font_montserratMedium_16)
except AttributeError:
    try:
        style_screen_btn_1_main_main_default.set_text_font(lv.font_montserrat_16)
    except AttributeError:
        style_screen_btn_1_main_main_default.set_text_font(lv.font_montserrat_16)
style_screen_btn_1_main_main_default.set_text_align(lv.TEXT_ALIGN.CENTER)

# add style for screen_btn_1
screen_btn_1.add_style(style_screen_btn_1_main_main_default, lv.PART.MAIN|lv.STATE.DEFAULT)


# create screen_btn_2
screen_btn_2 = lv.btn(screen)
screen_btn_2.set_pos(int(398),int(6))
screen_btn_2.set_size(65,35)
screen_btn_2.set_scrollbar_mode(lv.SCROLLBAR_MODE.OFF)
screen_btn_2_label = lv.label(screen_btn_2)
screen_btn_2_label.set_text("Setting")
screen_btn_2.set_style_pad_all(0, lv.STATE.DEFAULT)
screen_btn_2_label.align(lv.ALIGN.CENTER,0,0)
# create style style_screen_btn_2_main_main_default
style_screen_btn_2_main_main_default = lv.style_t()
style_screen_btn_2_main_main_default.init()
style_screen_btn_2_main_main_default.set_radius(5)
style_screen_btn_2_main_main_default.set_bg_color(lv.color_make(0x21,0x95,0xf6))
style_screen_btn_2_main_main_default.set_bg_grad_color(lv.color_make(0x21,0x95,0xf6))
style_screen_btn_2_main_main_default.set_bg_grad_dir(lv.GRAD_DIR.NONE)
style_screen_btn_2_main_main_default.set_bg_opa(255)
style_screen_btn_2_main_main_default.set_border_color(lv.color_make(0x21,0x95,0xf6))
style_screen_btn_2_main_main_default.set_border_width(0)
style_screen_btn_2_main_main_default.set_border_opa(255)
style_screen_btn_2_main_main_default.set_text_color(lv.color_make(0xff,0xff,0xff))
try:
    style_screen_btn_2_main_main_default.set_text_font(lv.font_montserratMedium_16)
except AttributeError:
    try:
        style_screen_btn_2_main_main_default.set_text_font(lv.font_montserrat_16)
    except AttributeError:
        style_screen_btn_2_main_main_default.set_text_font(lv.font_montserrat_16)
style_screen_btn_2_main_main_default.set_text_align(lv.TEXT_ALIGN.CENTER)

# add style for screen_btn_2
screen_btn_2.add_style(style_screen_btn_2_main_main_default, lv.PART.MAIN|lv.STATE.DEFAULT)


# create screen_label_time
screen_label_time = lv.label(screen)
screen_label_time.set_pos(int(190),int(6))
screen_label_time.set_size(100,32)
screen_label_time.set_scrollbar_mode(lv.SCROLLBAR_MODE.OFF)
screen_label_time.set_text("000")
screen_label_time.set_long_mode(lv.label.LONG.WRAP)
# create style style_screen_label_time_main_main_default
style_screen_label_time_main_main_default = lv.style_t()
style_screen_label_time_main_main_default.init()
style_screen_label_time_main_main_default.set_radius(0)
style_screen_label_time_main_main_default.set_bg_color(lv.color_make(0x21,0x95,0xf6))
style_screen_label_time_main_main_default.set_bg_grad_color(lv.color_make(0x21,0x95,0xf6))
style_screen_label_time_main_main_default.set_bg_grad_dir(lv.GRAD_DIR.NONE)
style_screen_label_time_main_main_default.set_bg_opa(0)
style_screen_label_time_main_main_default.set_text_color(lv.color_make(0xff,0xff,0xff))
try:
    style_screen_label_time_main_main_default.set_text_font(lv.font_montserratMedium_26)
except AttributeError:
    try:
        style_screen_label_time_main_main_default.set_text_font(lv.font_montserrat_26)
    except AttributeError:
        style_screen_label_time_main_main_default.set_text_font(lv.font_montserrat_16)
style_screen_label_time_main_main_default.set_text_letter_space(2)
style_screen_label_time_main_main_default.set_text_line_space(0)
style_screen_label_time_main_main_default.set_text_align(lv.TEXT_ALIGN.CENTER)
style_screen_label_time_main_main_default.set_pad_left(0)
style_screen_label_time_main_main_default.set_pad_right(0)
style_screen_label_time_main_main_default.set_pad_top(0)
style_screen_label_time_main_main_default.set_pad_bottom(0)

# add style for screen_label_time
screen_label_time.add_style(style_screen_label_time_main_main_default, lv.PART.MAIN|lv.STATE.DEFAULT)


# create screen_label_2
screen_label_2 = lv.label(screen)
screen_label_2.set_pos(int(11),int(6))
screen_label_2.set_size(138,53)
screen_label_2.set_scrollbar_mode(lv.SCROLLBAR_MODE.OFF)
screen_label_2.set_text("Hits:\nMisses:\n")
screen_label_2.set_long_mode(lv.label.LONG.WRAP)
# create style style_screen_label_2_main_main_default
style_screen_label_2_main_main_default = lv.style_t()
style_screen_label_2_main_main_default.init()
style_screen_label_2_main_main_default.set_radius(0)
style_screen_label_2_main_main_default.set_bg_color(lv.color_make(0xf1,0x93,0xc0))
style_screen_label_2_main_main_default.set_bg_grad_color(lv.color_make(0x21,0x95,0xf6))
style_screen_label_2_main_main_default.set_bg_grad_dir(lv.GRAD_DIR.NONE)
style_screen_label_2_main_main_default.set_bg_opa(116)
style_screen_label_2_main_main_default.set_text_color(lv.color_make(0xff,0xff,0xff))
try:
    style_screen_label_2_main_main_default.set_text_font(lv.font_montserratMedium_20)
except AttributeError:
    try:
        style_screen_label_2_main_main_default.set_text_font(lv.font_montserrat_20)
    except AttributeError:
        style_screen_label_2_main_main_default.set_text_font(lv.font_montserrat_16)
style_screen_label_2_main_main_default.set_text_letter_space(2)
style_screen_label_2_main_main_default.set_text_line_space(0)
style_screen_label_2_main_main_default.set_text_align(lv.TEXT_ALIGN.LEFT)
style_screen_label_2_main_main_default.set_pad_left(0)
style_screen_label_2_main_main_default.set_pad_right(0)
style_screen_label_2_main_main_default.set_pad_top(8)
style_screen_label_2_main_main_default.set_pad_bottom(0)

# add style for screen_label_2
screen_label_2.add_style(style_screen_label_2_main_main_default, lv.PART.MAIN|lv.STATE.DEFAULT)


# create screen_label_3
screen_label_3 = lv.label(screen)
screen_label_3.set_pos(int(62),int(6))
screen_label_3.set_size(57,31)
screen_label_3.set_scrollbar_mode(lv.SCROLLBAR_MODE.OFF)
screen_label_3.set_text("0")
screen_label_3.set_long_mode(lv.label.LONG.WRAP)
# create style style_screen_label_3_main_main_default
style_screen_label_3_main_main_default = lv.style_t()
style_screen_label_3_main_main_default.init()
style_screen_label_3_main_main_default.set_radius(0)
style_screen_label_3_main_main_default.set_bg_color(lv.color_make(0x21,0x95,0xf6))
style_screen_label_3_main_main_default.set_bg_grad_color(lv.color_make(0x21,0x95,0xf6))
style_screen_label_3_main_main_default.set_bg_grad_dir(lv.GRAD_DIR.NONE)
style_screen_label_3_main_main_default.set_bg_opa(0)
style_screen_label_3_main_main_default.set_text_color(lv.color_make(0xff,0xff,0xff))
try:
    style_screen_label_3_main_main_default.set_text_font(lv.font_montserratMedium_20)
except AttributeError:
    try:
        style_screen_label_3_main_main_default.set_text_font(lv.font_montserrat_20)
    except AttributeError:
        style_screen_label_3_main_main_default.set_text_font(lv.font_montserrat_16)
style_screen_label_3_main_main_default.set_text_letter_space(2)
style_screen_label_3_main_main_default.set_text_line_space(0)
style_screen_label_3_main_main_default.set_text_align(lv.TEXT_ALIGN.CENTER)
style_screen_label_3_main_main_default.set_pad_left(0)
style_screen_label_3_main_main_default.set_pad_right(0)
style_screen_label_3_main_main_default.set_pad_top(8)
style_screen_label_3_main_main_default.set_pad_bottom(0)

# add style for screen_label_3
screen_label_3.add_style(style_screen_label_3_main_main_default, lv.PART.MAIN|lv.STATE.DEFAULT)


# create screen_label_4
screen_label_4 = lv.label(screen)
screen_label_4.set_pos(int(92),int(28))
screen_label_4.set_size(54,31)
screen_label_4.set_scrollbar_mode(lv.SCROLLBAR_MODE.OFF)
screen_label_4.set_text("0")
screen_label_4.set_long_mode(lv.label.LONG.WRAP)
# create style style_screen_label_4_main_main_default
style_screen_label_4_main_main_default = lv.style_t()
style_screen_label_4_main_main_default.init()
style_screen_label_4_main_main_default.set_radius(0)
style_screen_label_4_main_main_default.set_bg_color(lv.color_make(0x21,0x95,0xf6))
style_screen_label_4_main_main_default.set_bg_grad_color(lv.color_make(0x21,0x95,0xf6))
style_screen_label_4_main_main_default.set_bg_grad_dir(lv.GRAD_DIR.NONE)
style_screen_label_4_main_main_default.set_bg_opa(0)
style_screen_label_4_main_main_default.set_text_color(lv.color_make(0xff,0xff,0xff))
try:
    style_screen_label_4_main_main_default.set_text_font(lv.font_montserratMedium_20)
except AttributeError:
    try:
        style_screen_label_4_main_main_default.set_text_font(lv.font_montserrat_20)
    except AttributeError:
        style_screen_label_4_main_main_default.set_text_font(lv.font_montserrat_16)
style_screen_label_4_main_main_default.set_text_letter_space(2)
style_screen_label_4_main_main_default.set_text_line_space(0)
style_screen_label_4_main_main_default.set_text_align(lv.TEXT_ALIGN.CENTER)
style_screen_label_4_main_main_default.set_pad_left(0)
style_screen_label_4_main_main_default.set_pad_right(0)
style_screen_label_4_main_main_default.set_pad_top(8)
style_screen_label_4_main_main_default.set_pad_bottom(0)

# add style for screen_label_4
screen_label_4.add_style(style_screen_label_4_main_main_default, lv.PART.MAIN|lv.STATE.DEFAULT)


# create screen_tabview_1
screen_tabview_1 = lv.tabview(screen, lv.DIR.TOP, 50)
screen_tabview_1_tab_btns = screen_tabview_1.get_tab_btns()
# create style style_screen_tabview_1_extra_btnm_main_default
style_screen_tabview_1_extra_btnm_main_default = lv.style_t()
style_screen_tabview_1_extra_btnm_main_default.init()
style_screen_tabview_1_extra_btnm_main_default.set_radius(0)
style_screen_tabview_1_extra_btnm_main_default.set_bg_color(lv.color_make(0xff,0xff,0xff))
style_screen_tabview_1_extra_btnm_main_default.set_bg_grad_color(lv.color_make(0xff,0xff,0xff))
style_screen_tabview_1_extra_btnm_main_default.set_bg_grad_dir(lv.GRAD_DIR.NONE)
style_screen_tabview_1_extra_btnm_main_default.set_bg_opa(255)
style_screen_tabview_1_extra_btnm_main_default.set_border_color(lv.color_make(0x21,0x95,0xf6))
style_screen_tabview_1_extra_btnm_main_default.set_border_width(0)
style_screen_tabview_1_extra_btnm_main_default.set_border_opa(100)

# add style for screen_tabview_1_tab_btns
screen_tabview_1_tab_btns.add_style(style_screen_tabview_1_extra_btnm_main_default, lv.PART.MAIN|lv.STATE.DEFAULT)

# create style style_screen_tabview_1_extra_btnm_items_default
style_screen_tabview_1_extra_btnm_items_default = lv.style_t()
style_screen_tabview_1_extra_btnm_items_default.init()
style_screen_tabview_1_extra_btnm_items_default.set_text_color(lv.color_make(0x4d,0x4d,0x4d))
try:
    style_screen_tabview_1_extra_btnm_items_default.set_text_font(lv.font_montserratMedium_12)
except AttributeError:
    try:
        style_screen_tabview_1_extra_btnm_items_default.set_text_font(lv.font_montserrat_12)
    except AttributeError:
        style_screen_tabview_1_extra_btnm_items_default.set_text_font(lv.font_montserrat_16)

# add style for screen_tabview_1_tab_btns
screen_tabview_1_tab_btns.add_style(style_screen_tabview_1_extra_btnm_items_default, lv.PART.ITEMS|lv.STATE.DEFAULT)

# create style style_screen_tabview_1_extra_btnm_items_checked
style_screen_tabview_1_extra_btnm_items_checked = lv.style_t()
style_screen_tabview_1_extra_btnm_items_checked.init()
style_screen_tabview_1_extra_btnm_items_checked.set_radius(0)
style_screen_tabview_1_extra_btnm_items_checked.set_bg_color(lv.color_make(0x21,0x95,0xf6))
style_screen_tabview_1_extra_btnm_items_checked.set_bg_grad_color(lv.color_make(0x21,0x95,0xf6))
style_screen_tabview_1_extra_btnm_items_checked.set_bg_grad_dir(lv.GRAD_DIR.NONE)
style_screen_tabview_1_extra_btnm_items_checked.set_bg_opa(60)
style_screen_tabview_1_extra_btnm_items_checked.set_border_color(lv.color_make(0x21,0x95,0xf6))
style_screen_tabview_1_extra_btnm_items_checked.set_border_width(4)
style_screen_tabview_1_extra_btnm_items_checked.set_border_opa(255)
style_screen_tabview_1_extra_btnm_items_checked.set_border_side(lv.BORDER_SIDE.BOTTOM)
style_screen_tabview_1_extra_btnm_items_checked.set_text_color(lv.color_make(0x21,0x95,0xf6))
try:
    style_screen_tabview_1_extra_btnm_items_checked.set_text_font(lv.font_montserratMedium_12)
except AttributeError:
    try:
        style_screen_tabview_1_extra_btnm_items_checked.set_text_font(lv.font_montserrat_12)
    except AttributeError:
        style_screen_tabview_1_extra_btnm_items_checked.set_text_font(lv.font_montserrat_16)

# add style for screen_tabview_1_tab_btns
screen_tabview_1_tab_btns.add_style(style_screen_tabview_1_extra_btnm_items_checked, lv.PART.ITEMS|lv.STATE.CHECKED)

screen_tabview_1_Speed = screen_tabview_1.add_tab("Speed")

# create screen_slider_1
screen_slider_1 = lv.slider(screen_tabview_1_Speed)
screen_slider_1.set_pos(int(4),int(1))
screen_slider_1.set_size(187,14)
screen_slider_1.set_scrollbar_mode(lv.SCROLLBAR_MODE.OFF)
screen_slider_1.set_range(0, 100)
screen_slider_1.set_value(50, False)

# create style style_screen_slider_1_main_main_default
style_screen_slider_1_main_main_default = lv.style_t()
style_screen_slider_1_main_main_default.init()
style_screen_slider_1_main_main_default.set_radius(50)
style_screen_slider_1_main_main_default.set_bg_color(lv.color_make(0x21,0x95,0xf6))
style_screen_slider_1_main_main_default.set_bg_grad_color(lv.color_make(0x21,0x95,0xf6))
style_screen_slider_1_main_main_default.set_bg_grad_dir(lv.GRAD_DIR.NONE)
style_screen_slider_1_main_main_default.set_bg_opa(60)
style_screen_slider_1_main_main_default.set_outline_color(lv.color_make(0xeb,0x7f,0xb8))
style_screen_slider_1_main_main_default.set_outline_width(0)
style_screen_slider_1_main_main_default.set_outline_opa(255)

# add style for screen_slider_1
screen_slider_1.add_style(style_screen_slider_1_main_main_default, lv.PART.MAIN|lv.STATE.DEFAULT)

# create style style_screen_slider_1_main_indicator_default
style_screen_slider_1_main_indicator_default = lv.style_t()
style_screen_slider_1_main_indicator_default.init()
style_screen_slider_1_main_indicator_default.set_radius(50)
style_screen_slider_1_main_indicator_default.set_bg_color(lv.color_make(0xdf,0xe4,0x33))
style_screen_slider_1_main_indicator_default.set_bg_grad_color(lv.color_make(0x21,0x95,0xf6))
style_screen_slider_1_main_indicator_default.set_bg_grad_dir(lv.GRAD_DIR.NONE)
style_screen_slider_1_main_indicator_default.set_bg_opa(255)

# add style for screen_slider_1
screen_slider_1.add_style(style_screen_slider_1_main_indicator_default, lv.PART.INDICATOR|lv.STATE.DEFAULT)

# create style style_screen_slider_1_main_knob_default
style_screen_slider_1_main_knob_default = lv.style_t()
style_screen_slider_1_main_knob_default.init()
style_screen_slider_1_main_knob_default.set_radius(50)
style_screen_slider_1_main_knob_default.set_bg_color(lv.color_make(0xf1,0x9b,0xd2))
style_screen_slider_1_main_knob_default.set_bg_grad_color(lv.color_make(0x21,0x95,0xf6))
style_screen_slider_1_main_knob_default.set_bg_grad_dir(lv.GRAD_DIR.NONE)
style_screen_slider_1_main_knob_default.set_bg_opa(255)

# add style for screen_slider_1
screen_slider_1.add_style(style_screen_slider_1_main_knob_default, lv.PART.KNOB|lv.STATE.DEFAULT)


# create screen_label_5
screen_label_5 = lv.label(screen_tabview_1_Speed)
screen_label_5.set_pos(int(49),int(29))
screen_label_5.set_size(100,32)
screen_label_5.set_scrollbar_mode(lv.SCROLLBAR_MODE.OFF)
screen_label_5.set_text("50")
screen_label_5.set_long_mode(lv.label.LONG.WRAP)
# create style style_screen_label_5_main_main_default
style_screen_label_5_main_main_default = lv.style_t()
style_screen_label_5_main_main_default.init()
style_screen_label_5_main_main_default.set_radius(0)
style_screen_label_5_main_main_default.set_bg_color(lv.color_make(0x21,0x95,0xf6))
style_screen_label_5_main_main_default.set_bg_grad_color(lv.color_make(0x21,0x95,0xf6))
style_screen_label_5_main_main_default.set_bg_grad_dir(lv.GRAD_DIR.NONE)
style_screen_label_5_main_main_default.set_bg_opa(0)
style_screen_label_5_main_main_default.set_text_color(lv.color_make(0x00,0x00,0x00))
try:
    style_screen_label_5_main_main_default.set_text_font(lv.font_montserratMedium_16)
except AttributeError:
    try:
        style_screen_label_5_main_main_default.set_text_font(lv.font_montserrat_16)
    except AttributeError:
        style_screen_label_5_main_main_default.set_text_font(lv.font_montserrat_16)
style_screen_label_5_main_main_default.set_text_letter_space(2)
style_screen_label_5_main_main_default.set_text_line_space(0)
style_screen_label_5_main_main_default.set_text_align(lv.TEXT_ALIGN.CENTER)
style_screen_label_5_main_main_default.set_pad_left(0)
style_screen_label_5_main_main_default.set_pad_right(0)
style_screen_label_5_main_main_default.set_pad_top(8)
style_screen_label_5_main_main_default.set_pad_bottom(0)

# add style for screen_label_5
screen_label_5.add_style(style_screen_label_5_main_main_default, lv.PART.MAIN|lv.STATE.DEFAULT)

screen_tabview_1_Time = screen_tabview_1.add_tab("Time")

# create screen_label_6
screen_label_6 = lv.label(screen_tabview_1_Time)
screen_label_6.set_pos(int(49),int(29))
screen_label_6.set_size(100,32)
screen_label_6.set_scrollbar_mode(lv.SCROLLBAR_MODE.OFF)
screen_label_6.set_text("50")
screen_label_6.set_long_mode(lv.label.LONG.WRAP)
# create style style_screen_label_6_main_main_default
style_screen_label_6_main_main_default = lv.style_t()
style_screen_label_6_main_main_default.init()
style_screen_label_6_main_main_default.set_radius(0)
style_screen_label_6_main_main_default.set_bg_color(lv.color_make(0x21,0x95,0xf6))
style_screen_label_6_main_main_default.set_bg_grad_color(lv.color_make(0x21,0x95,0xf6))
style_screen_label_6_main_main_default.set_bg_grad_dir(lv.GRAD_DIR.NONE)
style_screen_label_6_main_main_default.set_bg_opa(0)
style_screen_label_6_main_main_default.set_text_color(lv.color_make(0x00,0x00,0x00))
try:
    style_screen_label_6_main_main_default.set_text_font(lv.font_montserratMedium_16)
except AttributeError:
    try:
        style_screen_label_6_main_main_default.set_text_font(lv.font_montserrat_16)
    except AttributeError:
        style_screen_label_6_main_main_default.set_text_font(lv.font_montserrat_16)
style_screen_label_6_main_main_default.set_text_letter_space(2)
style_screen_label_6_main_main_default.set_text_line_space(0)
style_screen_label_6_main_main_default.set_text_align(lv.TEXT_ALIGN.CENTER)
style_screen_label_6_main_main_default.set_pad_left(0)
style_screen_label_6_main_main_default.set_pad_right(0)
style_screen_label_6_main_main_default.set_pad_top(8)
style_screen_label_6_main_main_default.set_pad_bottom(0)

# add style for screen_label_6
screen_label_6.add_style(style_screen_label_6_main_main_default, lv.PART.MAIN|lv.STATE.DEFAULT)


# create screen_slider_2
screen_slider_2 = lv.slider(screen_tabview_1_Time)
screen_slider_2.set_pos(int(4),int(1))
screen_slider_2.set_size(187,14)
screen_slider_2.set_scrollbar_mode(lv.SCROLLBAR_MODE.OFF)
screen_slider_2.set_range(0, 100)
screen_slider_2.set_value(50, False)

# create style style_screen_slider_2_main_main_default
style_screen_slider_2_main_main_default = lv.style_t()
style_screen_slider_2_main_main_default.init()
style_screen_slider_2_main_main_default.set_radius(50)
style_screen_slider_2_main_main_default.set_bg_color(lv.color_make(0x21,0x95,0xf6))
style_screen_slider_2_main_main_default.set_bg_grad_color(lv.color_make(0x21,0x95,0xf6))
style_screen_slider_2_main_main_default.set_bg_grad_dir(lv.GRAD_DIR.NONE)
style_screen_slider_2_main_main_default.set_bg_opa(60)
style_screen_slider_2_main_main_default.set_outline_color(lv.color_make(0xeb,0x7f,0xb8))
style_screen_slider_2_main_main_default.set_outline_width(0)
style_screen_slider_2_main_main_default.set_outline_opa(255)

# add style for screen_slider_2
screen_slider_2.add_style(style_screen_slider_2_main_main_default, lv.PART.MAIN|lv.STATE.DEFAULT)

# create style style_screen_slider_2_main_indicator_default
style_screen_slider_2_main_indicator_default = lv.style_t()
style_screen_slider_2_main_indicator_default.init()
style_screen_slider_2_main_indicator_default.set_radius(50)
style_screen_slider_2_main_indicator_default.set_bg_color(lv.color_make(0xdf,0xe4,0x33))
style_screen_slider_2_main_indicator_default.set_bg_grad_color(lv.color_make(0x21,0x95,0xf6))
style_screen_slider_2_main_indicator_default.set_bg_grad_dir(lv.GRAD_DIR.NONE)
style_screen_slider_2_main_indicator_default.set_bg_opa(255)

# add style for screen_slider_2
screen_slider_2.add_style(style_screen_slider_2_main_indicator_default, lv.PART.INDICATOR|lv.STATE.DEFAULT)

# create style style_screen_slider_2_main_knob_default
style_screen_slider_2_main_knob_default = lv.style_t()
style_screen_slider_2_main_knob_default.init()
style_screen_slider_2_main_knob_default.set_radius(50)
style_screen_slider_2_main_knob_default.set_bg_color(lv.color_make(0xf1,0x9b,0xd2))
style_screen_slider_2_main_knob_default.set_bg_grad_color(lv.color_make(0x21,0x95,0xf6))
style_screen_slider_2_main_knob_default.set_bg_grad_dir(lv.GRAD_DIR.NONE)
style_screen_slider_2_main_knob_default.set_bg_opa(255)

# add style for screen_slider_2
screen_slider_2.add_style(style_screen_slider_2_main_knob_default, lv.PART.KNOB|lv.STATE.DEFAULT)

screen_tabview_1.set_pos(int(123),int(91))
screen_tabview_1.set_size(235,144)
screen_tabview_1.set_scrollbar_mode(lv.SCROLLBAR_MODE.OFF)
# create style style_screen_tabview_1_main_main_default
style_screen_tabview_1_main_main_default = lv.style_t()
style_screen_tabview_1_main_main_default.init()
style_screen_tabview_1_main_main_default.set_radius(0)
style_screen_tabview_1_main_main_default.set_bg_color(lv.color_make(0xff,0xff,0xff))
style_screen_tabview_1_main_main_default.set_bg_grad_color(lv.color_make(0xea,0xef,0xf3))
style_screen_tabview_1_main_main_default.set_bg_grad_dir(lv.GRAD_DIR.NONE)
style_screen_tabview_1_main_main_default.set_bg_opa(255)
style_screen_tabview_1_main_main_default.set_border_color(lv.color_make(0x13,0xda,0xfd))
style_screen_tabview_1_main_main_default.set_border_width(2)
style_screen_tabview_1_main_main_default.set_border_opa(255)
style_screen_tabview_1_main_main_default.set_text_color(lv.color_make(0xc9,0xe6,0x0f))
try:
    style_screen_tabview_1_main_main_default.set_text_font(lv.font_montserratMedium_12)
except AttributeError:
    try:
        style_screen_tabview_1_main_main_default.set_text_font(lv.font_montserrat_12)
    except AttributeError:
        style_screen_tabview_1_main_main_default.set_text_font(lv.font_montserrat_16)
style_screen_tabview_1_main_main_default.set_text_letter_space(2)
style_screen_tabview_1_main_main_default.set_text_line_space(16)

# add style for screen_tabview_1
screen_tabview_1.add_style(style_screen_tabview_1_main_main_default, lv.PART.MAIN|lv.STATE.DEFAULT)



def screen_btn_2_pressed_1_event_cb(e,screen_tabview_1):
    src = e.get_target()
    code = e.get_code()
    screen_tabview_1.set_pos(123, 115)
screen_btn_2.add_event_cb(lambda e: screen_btn_2_pressed_1_event_cb(e,screen_tabview_1), lv.EVENT.PRESSED, None)


def screen_btn_1_pressed_1_event_cb(e,screen_btn_1):
    src = e.get_target()
    code = e.get_code()
    screen_btn_1.set_style_bg_color(lv.color_make(0x00, 0x00, 0x00), lv.PART.MAIN)
screen_btn_1.add_event_cb(lambda e: screen_btn_1_pressed_1_event_cb(e,screen_btn_1), lv.EVENT.PRESSED, None)


def screen_slider_1_value_changed_1_event_cb(e,screen_label_4):
    src = e.get_target()
    code = e.get_code()
    try:
        screen_label_4.set_style_text_font(lv.font_simsun_12, lv.STATE.DEFAULT)
    except AttributeError:
        try:
            screen_label_4.set_style_text_font(lv.font_montserrat_12, lv.STATE.DEFAULT)
        except AttributeError:
            screen_label_4.set_style_text_font(lv.font_montserrat_16, lv.STATE.DEFAULT)
    screen_label_4.set_text("default")

screen_slider_1.add_event_cb(lambda e: screen_slider_1_value_changed_1_event_cb(e,screen_label_4), lv.EVENT.VALUE_CHANGED, None)


def screen_slider_2_value_changed_1_event_cb(e,screen_label_4):
    src = e.get_target()
    code = e.get_code()
    try:
        screen_label_4.set_style_text_font(lv.font_simsun_12, lv.STATE.DEFAULT)
    except AttributeError:
        try:
            screen_label_4.set_style_text_font(lv.font_montserrat_12, lv.STATE.DEFAULT)
        except AttributeError:
            screen_label_4.set_style_text_font(lv.font_montserrat_16, lv.STATE.DEFAULT)
    screen_label_4.set_text("default")

screen_slider_2.add_event_cb(lambda e: screen_slider_2_value_changed_1_event_cb(e,screen_label_4), lv.EVENT.VALUE_CHANGED, None)



# content from custom.py

# Load the default screen
lv.scr_load(screen)

while SDL.check():
    time.sleep_ms(5)
