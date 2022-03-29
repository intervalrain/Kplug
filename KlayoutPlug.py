# $autorun

import pya
import csv

def objAreaCal():
    view = pya.Application.instance().main_window().current_view()
    if view is None:
        pya.MessageBox.info("Alarm", "No view selected", pya.MessageBox.Ok)
    total_area = 0.0
    objs = view.object_selection
    for i in range(0, len(objs)):
        shape = objs[i].shape
        layout = view.cellview(objs[i].cv_index).layout()
        if shape.is_polygon() or shape.is_box() or shape_is_path():
            polygon = shape.polygon
            a = polygon.area()
            m = objs[i].trans().mag * layout.dbu
            total_area += a * m * m
    pya.MessageBox.info("Hint", "Total Object Area: " + str(total_area) + " (um.square)", pya.MessageBox.Ok)

def regAreaCal():
    view = pya.Application.instance().main_window().current_view()
    if view is None:
        pya.MessageBox.info("Alarm", "No view selected", pya.MessageBox.Ok)
    objs = view.object_selection
    region = pya.Region()
    for i in range(0, len(objs)):
        shape = objs[i].shape
        layout = view.cellview(objs[i].cv_index).layout()
        m = objs[0].trans().mag * layout.dbu
        if shape.is_polygon() or shape.is_box() or shape_is_path():
            region += objs[i].trans() * shape.polygon
            total_area = region.area() * m * m
    pya.MessageBox.info("Hint", "Total Region Area: " + str(total_area) + "(um.square)", pya.MessageBox.Ok)

def loadLyp():
    file_path = pya.FileDialog.ask_open_file_name("Load csv file...", "/Users/rainhu/temp", "*.csv")
    with open(file_path, newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter='\t')
        dict = {str(rows[1])+","+str(rows[2]):rows[0] for rows in reader}
    
    view = pya.LayoutView.current()
    iter = view.begin_layers()
    while not iter.at_end():
        node = iter.current()
        ly = view.cellview(node.cellview())
        key = str(node.source_layer) + "," + str(node.source_datatype)
        if key in dict.keys():
            node.name = dict[key]
        iter.next()

menu = pya.Application.instance().main_window().menu()
    
action_objAreaCal = pya.Action()
action_objAreaCal.title = "ObjAreaCal"
action_objAreaCal.on_triggered(objAreaCal)

action_regAreaCal = pya.Action()
action_regAreaCal.title = "RegAreaCal"
action_regAreaCal.on_triggered(regAreaCal)

action_loadLyp = pya.Action()
action_loadLyp.title = "LoadLyp"
action_loadLyp.on_triggered(loadLyp)

menu.insert_separator("@toolbar.end", "AreaCal")

menu.insert_item("@toolbar.end", "objAreaCal", action_objAreaCal)
menu.insert_item("@toolbar.end", "regAreaCal", action_regAreaCal)
menu.insert_item("@toolbar.end", "loadLyp", action_loadLyp)
