# $autorun

import pya
import csv
import os

# hide to avoid misleading
def objAreaCal():
    view = pya.Application.instance().main_window().current_view()
    if view is None:
        pya.MessageBox.info("Alarm", "No view selected", pya.MessageBox.Ok)
    total_area = 0.0
    objs = view.object_selection
    for i in range(0, len(objs)):
        shape = objs[i].shape
        layout = view.cellview(objs[i].cv_index).layout()
        if shape.is_polygon() or shape.is_box() or shape.is_path():
            polygon = shape.polygon
            a = polygon.area()
            m = objs[i].trans().mag * layout.dbu
            total_area += a * m * m
    pya.MessageBox.info("Hint", "Total Object Area: " + str(total_area) + " (um.square)", pya.MessageBox.Ok)

def regAreaCal():
    view = pya.Application.instance().main_window().current_view()
    
    # check gds is open
    if view is None:
        pya.MessageBox.info("Alarm", "No view selected", pya.MessageBox.Ok)
        return
    objs = view.object_selection
    region = pya.Region()
    for i in range(0, len(objs)):
        shape = objs[i].shape
        layout = view.cellview(objs[i].cv_index).layout()
        m = objs[0].trans().mag * layout.dbu
        if shape.is_polygon() or shape.is_box() or shape.is_path():
            region += objs[i].trans() * shape.polygon
            total_area = region.area() * m * m
    pya.MessageBox.info("Hint", "Total Region Area: " + format(total_area, ".3f") + "(um.square)", pya.MessageBox.Ok)

def perimeterCal():
    view = pya.Application.instance().main_window().current_view()

    # check gds is open
    if view is None:
        pya.MessageBox.info("Alarm", "No view selected", pya.MessageBox.Ok)
        return
    objs = view.object_selection
    region = pya.Region()
    for i in range(0, len(objs)):
        shape = objs[i].shape
        layout = view.cellview(objs[i].cv_index).layout()
        m = objs[0].trans().mag * layout.dbu
        if shape.is_polygon() or shape.is_box() or shape.is_path():
            region += objs[i].trans() * shape.polygon
            total_perimeter = region.perimeter() * m

            pya.MessageBox.info("Hint", "Total Region perimeter: " + format(total_perimeter, ".3f") + " (um)", pya.MessageBox.Ok)

def densityCal():
    view = pya.Application.instance().main_window().current_view()

    # check gds is open
    if view is None:
        pya.MessageBox.info("Alarm", "No view selected", pya.MessageBox.Ok)
        return

    # check the numbers of layers selected are exactly 2
    objs = view.object_selection
    layer_set = set();
    for i in range(len(objs)):
        layer_set.add(objs[i].layer)
    if len(layer_set) != 2:
        pya.MessageBox.info("Alarm", "Please select exactly 2 layers, not " + str(len(layer_set)) + " layers", pya.MessageBox.Ok)
        return

    # check if background covers all objects inside
    layer_list = list(layer_set)
    reg_back = pya.Region()
    reg_frnt = pya.Region()

    for i in range(len(objs)):
        if objs[i].layer == layer_list[0]:
            reg_back += objs[i].trans() * objs[i].shape.polygon
        if objs[i].layer == layer_list[1]:
            reg_frnt += objs[i].trans() * objs[i].shape.polygon

    reg_dummy = reg_back & reg_frnt
    reg_areaToCnt = reg_back if reg_back.area() > reg_dummy.area() else reg_frnt

    pya.MessageBox.info("Hint", "Density of selected area: " + format(reg_dummy.area()/reg_areaToCnt.area(), ".3%"), pya.MessageBox.Ok)

def exportCoordinate():
    file_path = pya.FileDialog.ask_save_file_name("Save coordinate file as ...", "", "*.csv")
    ly = pya.Application.instance().main_window().current_view().active_cellview().layout()
    if file_path == None:
        return
    
    # umc default gds number for text is [85, 0]
    input = ly.find_layer(85, 0)
    if input is None:
        pya.MessageBox.info("Alarm", "85/0 not found", pya.MessageBox.Ok)
        return
    
    si = ly.begin_shapes(ly.top_cell(), input)
    top_cell = ly.top_cell().name

    with open(file_path, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['TopCell', 'Text', 'X', 'Y', 'Rotation'])
        si = ly.top_cell().begin_shapes_rec(input)
        while not si.at_end():
            try:
                dirc = str(si.shape().text.trans)[:3].strip()
            except:
                pass
            text = si.shape().text
            bbox = si.shape().bbox().transformed(si.trans())
            if text is not None:
                writer.writerow([top_cell, text.string, format(bbox.left * ly.dbu, '.3f'), format(bbox.bottom * ly.dbu, '.3f'), dirc])
            si.next()

def loadLyp():

    # open default.csv as default option
    try:
        tmpAry = __file__.split('/')
        Dir = __file__.replace(tmpAry[len(tmpAry)-1], '')
        file_path = Dir + "default.csv"
        with open(file_path, newline='') as csvfile:
            reader = csv.reader(csvfile, delimiter=',')
            dict = {str(rows[1]) + "," + str(rows[2]) : rows[0] for rows in reader}
    
    except:
        # open File Dialog to select lyp file manually
        try:
            file_path = pya.FileDialog.ask_open_file_name("Load csv file...", "", "*.csv")
            with open(file_path, newline = '') as csvfile:
                reader = csv.reader(csvfile, delimeter = ',')
                dict = {str(rows[1]) + "," + str(rows[2]) : rows[0] for rows in reader}
        except:
            pya.MessageBox.info("Notice", "No file selected", pya.MessageBox.Ok)
    
    view = pya.LayoutView.current()
    iter = view.begin_layers()
    while not iter.at_end():
        node = iter.current()
        ly = view.cellview(node.cellview())
        key = str(node.source_layer) + "," + str(node.source_datatype)
        if key in dict.keys():
            node.name = str(node.source_layer) + "/" + str(node.source_datatype) + " " + str(dict[key])
            node.source_name = str(node.source_layer) + "/" + str(node.source_datatype) + " " + str(dict[key])
        iter.next()

menu = pya.Application.instance().main_window().menu()
    
#action_objAreaCal = pya.Action()
#action_objAreaCal.title = "ObjAreaCal"
#action_objAreaCal.on_triggered(objAreaCal)

action_regAreaCal = pya.Action()
action_regAreaCal.title = "AreaCal"
action_regAreaCal.on_triggered(regAreaCal)

action_perimeterCal = pya.Action()
action_perimeterCal.title = "PerimeterCal"
action_perimeterCal.on_triggered(perimeterCal)

action_densityCal = pya.Action()
action_densityCal.title = "DesityCal"
action_densityCal.on_triggered(densityCal)

action_exportCoordinate = pya.Action()
action_exportCoordinate.title = "ExportCoordinate"
action_exportCoordinate.on_triggered(exportCoordinate)

action_loadLyp = pya.Action()
action_loadLyp.title = "LoadLyp"
action_loadLyp.on_triggered(loadLyp)

menu.insert_separator("@toolbar.end", "ManualFunction")

#menu.insert_item("@toolbar.end", "objAreaCal", action_objAreaCal)
menu.insert_item("@toolbar.end", "AreaCal", action_regAreaCal)
menu.insert_item("@toolbar.end", "PerimeterCal", action_perimeterCal)
menu.insert_item("@toolbar.end", "DensityCal", action_densityCal)
menu.insert_item("@toolbar.end", "ExportCoordinate", action_exportCoordinate)
menu.insert_item("@toolbar.end", "loadLyp", action_loadLyp)
