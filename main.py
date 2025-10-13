#coding=utf-8
import sys
import re
import pandas as pd
import random
import os
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QLabel, QLineEdit, QPushButton, 
                             QTextEdit, QSpinBox, QComboBox, QMessageBox, 
                             QGroupBox, QGridLayout, QTabWidget, QFileDialog,
                             QInputDialog)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QPalette, QColor
from dataclasses import replace

import json
from json import load,dump


script_dir=os.path.dirname(os.path.abspath(__file__))
os.chdir(script_dir)
print(script_dir)

class FlightPlanGenerator(QMainWindow):
    def __init__(self):
        super().__init__()
        
        # 先定义所有属性
        self.airlines = ["AHK","BJN","BJV","CAO","CBJ","CCA","CCD","CCO","CDC","CDG","CES","CFA","CFI","CFJ","CGZ","CHB","CHH","CJG","CKK","CNM","CPA","CQH","CQN","CSC","CSG","CSH","CSN","CSS","CSZ","CUA","CXA","CYZ","CYN"]
        self.airports = ["ZBAA","ZBAD","ZBDS","ZBDT","ZBER","ZBHH","ZBLA","ZBMZ","ZBOW","ZBTJ","ZBYN","ZGDY","ZGGG","ZGHA","ZGKL","ZGNN","ZGOW","ZGSZ","ZHCC","ZHES","ZHHH","ZHYC","ZJHK","ZJQH","ZJSY","ZLDH","ZLIC","ZLLL","ZLXN","ZLXY","ZPJH","ZPLJ","ZPMS","ZPPP","ZSAM","ZSCG","ZSCN","ZSFZ","ZSHC","ZSJN","ZSLG","ZSLY","ZSNB","ZSNJ","ZSNT","ZSOF","ZSPD","ZSQD","ZSQZ","ZSSH","ZSSS","ZSTX","ZSWH","ZSWX","ZSWZ","ZSYA","ZSYN","ZSYT","ZSYW","ZSZS","ZUCK","ZUGY","ZULS","ZUTF","ZUUU","ZUXC","ZWSH","ZWTN","ZWWW","ZYCC","ZYHB","ZYJM","ZYMD","ZYQQ","ZYTL","ZYTX","ZYYJ"]
        self.ALTI = {"600":2000,"900":3000,"1200":3900,"1500":4900,"1800":5900,"2100":6900,"2400":7900,"2700":8900,"3000":9800,"3300":10800,"3600":11800,"3900":12800,"4200":13800,"4500":14800,"4800":15700,"5100":16700,"5400":17700,"5700":18700,"6000":19700,"6300":20700,"6600":21700,"6900":22600,"7200":23600,"7500":24600,"7800":25600,"8100":26600,"8400":27600,"8900":29100,"9200":30100,"9500":31100,"9800":32100,"10100":33100,"10400":34100,"10700":35100,"11000":36100,"11300":37100,"11600":38100,"11900":39100,"12200":40100,"12500":41100,"13100":43000,"13700":44900,"14300":46900,"14900":48900,"15500":50900}
        self.Cruise = {"29100":89,"30100":92,"31100":95,"32100":98,"33100":101,"34100":104,"35100":107,"36100":110,"37100":113,"38100":116,"39100":119,"40100":122,"41100":125}
        
        
        
        self.csv_path = "adf/RouteCheck.csv"
        self.gate_path="adf/Gate.json"
        
        # 然后初始化UI
        self.initUI()
        
    def initUI(self):
        self.setWindowTitle('模拟机文本生成器 v1.0')
        self.setGeometry(100, 100, 900, 700)
        
        # 设置应用样式
        self.setStyleSheet("""
            QMainWindow {
                background-color: #f0f0f0;
            }
            QGroupBox {
                font-weight: bold;
                border: 2px solid #cccccc;
                border-radius: 8px;
                margin-top: 1ex;
                padding-top: 10px;
                background-color: white;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px 0 5px;
                color: #2c3e50;
            }
            QPushButton {
                background-color: #3498db;
                border: none;
                color: white;
                padding: 8px 16px;
                border-radius: 4px;
                font-weight: bold;
                min-width: 100px;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
            QPushButton:pressed {
                background-color: #21618c;
            }
            QLineEdit, QComboBox, QSpinBox, QTextEdit {
                padding: 6px;
                border: 1px solid #bdc3c7;
                border-radius: 4px;
                background-color: white;
            }
            QLineEdit:focus, QComboBox:focus, QSpinBox:focus {
                border-color: #3498db;
            }
            QTabWidget::pane {
                border: 1px solid #bdc3c7;
                background-color: white;
            }
            QTabBar::tab {
                background-color: #ecf0f1;
                border: 1px solid #bdc3c7;
                padding: 8px 16px;
                margin-right: 2px;
                border-top-left-radius: 4px;
                border-top-right-radius: 4px;
            }
            QTabBar::tab:selected {
                background-color: #3498db;
                color: white;
            }
            QLabel {
                color: #2c3e50;
            }
        """)
        
        # 创建中心窗口和主布局
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        main_layout.setSpacing(15)
        main_layout.setContentsMargins(15, 15, 15, 15)
        
        # 创建标题
        title_label = QLabel("模拟机文本生成器")
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet("""
            QLabel {
                font-size: 20px;
                font-weight: bold;
                color: #2c3e50;
                padding: 10px;
                background-color: #3498db;
                color: white;
                border-radius: 5px;
            }
        """)
        main_layout.addWidget(title_label)
        
        # 创建选项卡
        tabs = QTabWidget()
        tabs.setStyleSheet("""
            QTabWidget::pane {
                border: 1px solid #bdc3c7;
                border-radius: 5px;
                background-color: white;
            }
        """)
        main_layout.addWidget(tabs)
        
        # 创建单个航班选项卡
        single_flight_tab = QWidget()
        single_layout = QVBoxLayout(single_flight_tab)
        single_layout.setSpacing(15)
        single_layout.setContentsMargins(15, 15, 15, 15)
        
        # 创建塔台航班选项卡
        tower_flight_tab = QWidget()
        tower_layout = QVBoxLayout(tower_flight_tab)
        tower_layout.setSpacing(15)
        tower_layout.setContentsMargins(15, 15, 15, 15)
        
        # 控制权设置
        control_group = QGroupBox("控制权设置")
        control_layout = QHBoxLayout(control_group)
        control_layout.addWidget(QLabel("控制权所有席位:"))
        self.ini_input = QLineEdit()
        self.ini_input.setPlaceholderText("请输入控制权席位...")
        control_layout.addWidget(self.ini_input)
        single_layout.addWidget(control_group)
        
        # 航班信息
        flight_group = QGroupBox("航班信息")
        flight_layout = QGridLayout(flight_group)
        flight_layout.setVerticalSpacing(10)
        flight_layout.setHorizontalSpacing(15)
        
        flight_layout.addWidget(QLabel("DEP机场:"), 0, 0)
        self.dep_input = QComboBox()
        self.dep_input.addItems(self.airports)
        self.dep_input.setEditable(True)
        flight_layout.addWidget(self.dep_input, 0, 1)
        
        flight_layout.addWidget(QLabel("ARR机场:"), 1, 0)
        self.arr_input = QComboBox()
        self.arr_input.addItems(self.airports)
        self.arr_input.setEditable(True)
        flight_layout.addWidget(self.arr_input, 1, 1)
        
        flight_layout.addWidget(QLabel("巡航高度:"), 2, 0)
        self.rfl_input = QComboBox()
        self.rfl_input.addItems(["29100", "30100", "31100", "32100", "33100", "34100", 
                                "35100", "36100", "37100", "38100", "39100", "40100", "41100"])
        flight_layout.addWidget(self.rfl_input, 2, 1)
        
        flight_layout.addWidget(QLabel("当前米制高度:"), 3, 0)
        self.alti_input = QComboBox()
        self.alti_input.addItems(list(self.ALTI.keys()))
        flight_layout.addWidget(self.alti_input, 3, 1)
        
        flight_layout.addWidget(QLabel("机型:"), 4, 0)
        self.typ_input = QLineEdit("A320")
        flight_layout.addWidget(self.typ_input, 4, 1)
        
        flight_layout.addWidget(QLabel("经纬度:"), 5, 0)
        self.pos_input = QLineEdit("N30.5,E120.5")
        self.pos_input.setPlaceholderText("格式: N30.5,E120.5")
        flight_layout.addWidget(self.pos_input, 5, 1)
        
        flight_layout.addWidget(QLabel("头朝向:"), 6, 0)
        head_layout = QHBoxLayout()
        self.head_input = QSpinBox()
        self.head_input.setRange(0, 360)
        self.head_input.setValue(0)
        head_layout.addWidget(self.head_input)
        head_layout.addStretch()
        flight_layout.addLayout(head_layout, 6, 1)
        
        flight_layout.addWidget(QLabel("实际航路:"), 7, 0)
        self.rte_input = QLineEdit()
        self.rte_input.setPlaceholderText("留空则使用数据库航路")
        flight_layout.addWidget(self.rte_input, 7, 1)
        
        single_layout.addWidget(flight_group)
        
        # 按钮区域
        button_group = QGroupBox("操作")
        button_layout = QHBoxLayout(button_group)
        self.generate_btn = QPushButton("生成飞行计划")
        self.generate_btn.clicked.connect(self.generate_single_flight)
        self.generate_btn.setStyleSheet("QPushButton { background-color: #27ae60; } QPushButton:hover { background-color: #219653; }")
        button_layout.addWidget(self.generate_btn)
        
        self.save_btn = QPushButton("保存到文件")
        self.save_btn.clicked.connect(self.save_to_file)
        self.save_btn.setStyleSheet("QPushButton { background-color: #e67e22; } QPushButton:hover { background-color: #d35400; }")
        button_layout.addWidget(self.save_btn)
        
        single_layout.addWidget(button_group)
        
        # 输出区域
        output_group = QGroupBox("输出")
        output_layout = QVBoxLayout(output_group)
        self.output_text = QTextEdit()
        self.output_text.setMinimumHeight(200)
        output_layout.addWidget(self.output_text)
        single_layout.addWidget(output_group)
        
        # 批量航班选项卡
        batch_flight_tab = QWidget()
        batch_layout = QVBoxLayout(batch_flight_tab)
        batch_layout.setSpacing(15)
        batch_layout.setContentsMargins(15, 15, 15, 15)
        
        batch_group = QGroupBox("批量生成设置")
        batch_grid = QGridLayout(batch_group)
        batch_grid.setVerticalSpacing(10)
        batch_grid.setHorizontalSpacing(15)
        
        batch_grid.addWidget(QLabel("机组数量:"), 0, 0)
        self.batch_count = QSpinBox()
        self.batch_count.setRange(1, 100)
        self.batch_count.setValue(5)
        batch_grid.addWidget(self.batch_count, 0, 1)
        
        batch_grid.addWidget(QLabel("控制权所有席位:"), 1, 0)
        self.batch_ini = QLineEdit()
        self.batch_ini.setPlaceholderText("请输入控制权席位...")
        batch_grid.addWidget(self.batch_ini, 1, 1)
        
        batch_layout.addWidget(batch_group)
        
        batch_button_group = QGroupBox("操作")
        batch_button_layout = QHBoxLayout(batch_button_group)
        self.batch_generate_btn = QPushButton("批量生成")
        self.batch_generate_btn.clicked.connect(self.generate_batch_flights)
        self.batch_generate_btn.setStyleSheet("QPushButton { background-color: #27ae60; } QPushButton:hover { background-color: #219653; }")
        batch_button_layout.addWidget(self.batch_generate_btn)
        batch_layout.addWidget(batch_button_group)
        
        batch_output_group = QGroupBox("批量输出")
        batch_output_layout = QVBoxLayout(batch_output_group)
        self.batch_output = QTextEdit()
        self.batch_output.setMinimumHeight(300)
        batch_output_layout.addWidget(self.batch_output)
        batch_layout.addWidget(batch_output_group)
        
        # 塔台选项卡
        # 控制权设置
        control_grooup = QGroupBox("控制权设置")
        control_layout = QHBoxLayout(control_grooup)
        control_layout.addWidget(QLabel("控制权所有席位:"))
        self.tower_ini_input = QLineEdit()
        self.tower_ini_input.setPlaceholderText("请输入控制权席位...")
        control_layout.addWidget(self.tower_ini_input)
        tower_layout.addWidget(control_grooup)
        
        # 航班信息
        flight_grooup = QGroupBox("航班信息")
        flight_layout = QGridLayout(flight_grooup)
        flight_layout.setVerticalSpacing(10)
        flight_layout.setHorizontalSpacing(15)
        
        flight_layout.addWidget(QLabel("DEP机场:"), 0, 0)
        self.tower_dep_input = QComboBox()
        self.tower_dep_input.setEditable(True)
        self.tower_dep_input.addItems(self.airports)
        flight_layout.addWidget(self.tower_dep_input, 0, 1)
        
        flight_layout.addWidget(QLabel("ARR机场:"), 1, 0)
        self.tower_arr_input = QComboBox()
        self.tower_arr_input.setEditable(True)
        self.tower_arr_input.addItems(self.airports)
        flight_layout.addWidget(self.tower_arr_input, 1, 1)
        
        flight_layout.addWidget(QLabel("巡航高度:"), 2, 0)
        self.tower_rfl_input = QComboBox()
        self.tower_rfl_input.addItems(["29100", "30100", "31100", "32100", "33100", "34100", 
                                "35100", "36100", "37100", "38100", "39100", "40100", "41100"])
        flight_layout.addWidget(self.tower_rfl_input, 2, 1)
        
        flight_layout.addWidget(QLabel("机场标高高度:"), 3, 0)
        self.tower_alti_input = QComboBox()
        self.tower_alti_input.addItems(list(self.ALTI.keys()))
        flight_layout.addWidget(self.tower_alti_input, 3, 1)
        
        flight_layout.addWidget(QLabel("机型:"), 4, 0)
        self.tower_typ_input = QLineEdit("A320")
        flight_layout.addWidget(self.tower_typ_input, 4, 1)
        
        flight_layout.addWidget(QLabel("机位:"), 5, 0)
        self.gate_input = QLineEdit("")
        self.gate_input.setPlaceholderText("请输入登机口...")
        flight_layout.addWidget(self.gate_input, 5, 1)
        
        flight_layout.addWidget(QLabel("实际航路:"), 6, 0)
        self.tower_rte_input = QLineEdit()
        self.tower_rte_input.setPlaceholderText("留空则使用数据库航路")
        flight_layout.addWidget(self.tower_rte_input, 6, 1)
        
        tower_layout.addWidget(flight_grooup)
        
        # 按钮
        tower_button_group = QGroupBox("操作")
        tower_button_layout = QHBoxLayout(tower_button_group)
        self.tower_generate_btn = QPushButton("生成飞行计划")
        self.tower_generate_btn.clicked.connect(self.generate_tower_flights)
        self.tower_generate_btn.setStyleSheet("QPushButton { background-color: #27ae60; } QPushButton:hover { background-color: #219653; }")
        tower_button_layout.addWidget(self.tower_generate_btn)
        
        self.tower_save_btn = QPushButton("保存到文件")
        self.tower_save_btn.clicked.connect(self.save_to_file)
        self.tower_save_btn.setStyleSheet("QPushButton { background-color: #e67e22; } QPushButton:hover { background-color: #d35400; }")
        tower_button_layout.addWidget(self.tower_save_btn)
        
        tower_layout.addWidget(tower_button_group)
        
        # 输出区域
        tower_output_group = QGroupBox("输出")
        tower_output_layout = QVBoxLayout(tower_output_group)
        self.tower_output = QTextEdit()
        self.tower_output.setMinimumHeight(200)
        tower_output_layout.addWidget(self.tower_output)
        tower_layout.addWidget(tower_output_group)
        
        # 添加选项卡
        tabs.addTab(single_flight_tab, "📝 单个航班")
        tabs.addTab(batch_flight_tab, "📊 批量生成")
        tabs.addTab(tower_flight_tab, "🏢 塔台设置")
        
        # 状态栏
        self.statusBar().showMessage("就绪 - 模拟机文本生成器已启动")
        
    def find_route_by_dep_arr(self, dep_code, arr_code):
        try:
            df = pd.read_csv(self.csv_path)
            
            if not all(col in df.columns for col in ['Dep', 'Arr', 'Route']):
                raise ValueError("CSV文件必须包含Dep, Arr和Route列")
            
            matched_routes = df[(df['Dep'] == dep_code) & (df['Arr'] == arr_code)].head(1)
            
            if not matched_routes.empty:
                return matched_routes['Route'].iloc[0], True
            else:
                dep_exists = (df['Dep'] == dep_code).any()
                arr_exists = (df['Arr'] == arr_code).any()
                
                if not dep_exists and not arr_exists:
                    QMessageBox.warning(self, "警告", f"数据库中既不存在Dep代码'{dep_code}'，也不存在Arr代码'{arr_code}'")
                elif not dep_exists:
                    QMessageBox.warning(self, "警告", f"数据库中不存在Dep代码'{dep_code}'")
                elif not arr_exists:
                    QMessageBox.warning(self, "警告", f"数据库中不存在Arr代码'{arr_code}'")
                
                return "", False
                
        except Exception as e:
            QMessageBox.critical(self, "错误", f"处理CSV文件时出错: {e}")
            return "", False
            
    def find_remarks_by_dep_arr(self, dep_code, arr_code):
        try:
            df = pd.read_csv(self.csv_path)
            
            if not all(col in df.columns for col in ['Dep', 'Arr', 'Remarks']):
                raise ValueError("CSV文件必须包含Dep, Arr和Remarks列")
            
            matched_remarks = df[(df['Dep'] == dep_code) & (df['Arr'] == arr_code)].head(1)
            
            if not matched_remarks.empty:
                remarks = matched_remarks['Remarks'].iloc[0]
                return str(remarks) if pd.notna(remarks) else ""
            else:
                return ""
                
        except Exception as e:
            QMessageBox.critical(self, "错误", f"处理CSV文件时出错: {e}")
            return ""
    
    def find_pos_and_hdg_by_gate(self, adep=None, gate=None):
        """
        根据机场和登机口查找位置和航向

        Args:
            adep: 机场ICAO代码,如果为None则使用界面输入
            gate: 登机口名称,如果为None则使用界面输入

        Returns:
            tuple: (位置, 航向) 或 None(如果未找到)
        """
        # 如果参数为空，从界面获取
        if adep is None:
            adep = self.tower_dep_input.currentText().strip()
        if gate is None:
            gate = self.gate_input.text().strip()

        # 验证输入
        if not adep or not gate:
            print("错误: 机场或登机口不能为空")
            return None

        try:
            with open(self.gate_path, "r", encoding="utf-8") as f:
                gt = json.load(f)

            # 检查机场是否存在
            if adep not in gt:
                print(f"错误: 机场 {adep} 不存在于数据中")
                return None

            airport = gt[adep]

            # 检查登机口是否存在
            if gate not in airport:
                print(f"错误: 登机口 {gate} 在机场 {adep} 中不存在")
                return None

            gates = airport[gate]

            # 检查必要字段
            if "pos" not in gates or "hdg" not in gates:
                print(f"错误: 登机口 {gate} 数据不完整，缺少 pos 或 hdg 字段")
                return None

            pos = gates["pos"]
            hdg = gates["hdg"]

            return pos, hdg

        except FileNotFoundError:
            print(f"错误: 文件 {self.gate_path} 不存在")
            return None
        except json.JSONDecodeError:
            print(f"错误: 文件 {self.gate_path} 格式错误")
            return None
        except Exception as e:
            print(f"未知错误: {e}")
            return None
   

    def write_pos_and_hdg_into_json(self, pos, hdg):
        """将位置和航向写入JSON文件"""
        adep = self.tower_dep_input.currentText().strip()
        gate = self.gate_input.text().strip()

        # 验证输入
        if not adep or not gate:
            print("错误: 机场或登机口不能为空")
            return False

        try:
            # 读取现有数据
            try:
                with open("Gate.json", "r", encoding="utf-8") as f:
                    data = json.load(f)
            except FileNotFoundError:
                # 如果文件不存在，创建空字典
                data = {}
            except json.JSONDecodeError:
                # 如果JSON格式错误，创建空字典
                print("JSON文件格式错误，将创建新文件")
                data = {}

            # 构建要添加的数据
            gate_data = {
                "pos": pos,
                "hdg": hdg
            }

            # 更新数据
            if adep in data:
                data[adep][gate] = gate_data
            else:
                data[adep] = {gate: gate_data}

            # 写回文件
            with open("Gate.json", "w", encoding="utf-8") as f:
                json.dump(data, f, indent=4, ensure_ascii=False)

            print(f"成功写入数据: {adep}/{gate} - 位置: {pos}, 航向: {hdg}")
            return True

        except Exception as e:
            print(f"写入数据时出错: {e}")
            return False
            
    def generate_single_flight(self):
        # 获取输入值
        airline = random.choice(self.airlines)
        numbers = str(random.randint(100,9999))
        callsign = airline + numbers
        adep = self.dep_input.currentText()
        dest = self.arr_input.currentText()
        rfl = self.rfl_input.currentText()
        alti_key = self.alti_input.currentText()
        alt = self.ALTI[alti_key]
        typ = self.typ_input.text()
        ppos = self.pos_input.text()
        head = self.head_input.value()
        hdg = int(head * 2.88 * 4 + 2)
        pos = ppos.replace(",", ":")
        if self.Cruise[str(rfl)]%2==0:
            EO="SE"
        else:
            EO="SO"
        Name=str(adep)+"-"+str(dest)
        
        # 查找航路
        route, found = self.find_route_by_dep_arr(adep, dest)
        if not found:
            reply = QMessageBox.question(self, "未找到航路", 
                                        f"未找到从{adep}到{dest}的路线,是否手动输入?",
                                        QMessageBox.Yes | QMessageBox.No)
            if reply == QMessageBox.Yes:
                route, ok = QInputDialog.getText(self, "手动输入航路", "请输入航路:")
                with open(self.csv_path,"a",encoding='utf-8') as file:
                    file.write('{},{},{},{},,,{},\n'.format(adep,dest,Name,EO,route))
                if not ok or not route:
                    return
            else:
                return
                
        remark = self.find_remarks_by_dep_arr(adep, dest)
        rte = self.rte_input.text() or route
        
        # 生成输出
        output = f"PSEUDOPILOT:ALL\n"
        output += f"@N:{callsign}:2000:1:{pos}:{alt}:0:{hdg}:0\n"
        output += f"$FP{callsign}:*A:I:{typ}:420:{adep}:0000:0000:{rfl}:{dest}:00:00:0:0::/v/{remark}:{route}\n"
        output += f"$ROUTE:{rte}\n"
        output += f"DELAY:1:8\n"
        output += f"REQALT::{alt}\n"
        output += f"INITIALPSEUDOPILOT:{self.ini_input.text()}\n"
        output += f"\n"
        
        self.output_text.setPlainText(output)
        self.statusBar().showMessage("单个航班计划生成完成")
        
    def generate_batch_flights(self):
        flights = self.batch_count.value()
        ini = self.batch_ini.text()
        
        output = "PSEUDOPILOT:ALL\n\n"
        
        for i in range(flights):
            airline = random.choice(self.airlines)
            numbers = str(random.randint(100,9999))
            callsign = airline + numbers
            
            # 随机选择不同的起降机场
            adep, dest = random.sample(self.airports, 2)
            
            rfl = random.choice(list(self.Cruise.keys()))
            alti_key = random.choice(list(self.ALTI.keys()))
            alt = self.ALTI[alti_key]
            typ = "A320"  # 默认机型
            ppos = "N30.5,E120.5"  # 默认位置
            head = random.randint(0, 360)
            hdg = int(head * 2.88 * 4 + 2)
            pos = ppos.replace(",", ":")
            
            # 查找航路
            route, found = self.find_route_by_dep_arr(adep, dest)
            if not found:
                route = "DIRECT"  # 默认航路
                
            remark = self.find_remarks_by_dep_arr(adep, dest)
            
            # 生成输出
            output += f"PSEUDOPILOT:ALL\n"
            output += f"@N:{callsign}:2000:1:{pos}:{alt}:0:{hdg}:0\n"
            output += f"$FP{callsign}:*A:I:{typ}:420:{adep}:0000:0000:{rfl}:{dest}:00:00:0:0::/v/{remark}:{route}\n"
            output += f"$ROUTE:{route}\n"
            output += f"DELAY:1:8\n"
            output += f"REQALT::{alt}\n"
            output += f"INITIALPSEUDOPILOT:{ini}\n"
            output += f"\n"
        
        self.batch_output.setPlainText(output)
        self.statusBar().showMessage(f"批量生成完成 - 共生成 {flights} 个航班计划")
    
    def generate_tower_flights(self):
        airline = random.choice(self.airlines)
        numbers = str(random.randint(100,9999))
        callsign = airline + numbers
        adep = self.tower_dep_input.currentText()
        dest = self.tower_arr_input.currentText()
        rfl = self.tower_rfl_input.currentText()
        alti_key = self.tower_alti_input.currentText()
        alt = self.ALTI[alti_key]
        typ = self.tower_typ_input.text()
        gate = self.gate_input.text()
        result = self.find_pos_and_hdg_by_gate(adep, gate)
        if result:
                pos, hdg = result
        else:
                reply = QMessageBox.question(self, "未找到登机口数据", f"未找到{adep}的{gate}数据，是否手动输入？",
                                           QMessageBox.Yes | QMessageBox.No)
                if reply == QMessageBox.Yes:
                    pos, ok = QInputDialog.getText(self, "手动输入登机口数据", "请输入经纬度:")
                    if not ok or not pos:
                        return
                    hdg, ok = QInputDialog.getInt(self, "手动输入登机口数据", "请输入头朝向:", 0, 0, 360, 1)
                    if not ok:
                        return
                    self.write_pos_and_hdg_into_json(pos, str(hdg))
                else:
                    return
        pos = pos.replace(",", ":")
        hdg = str(int(hdg) * 2.88 * 4 + 2)
        if self.Cruise[str(rfl)]%2==0:
            EO="SE"
        else:
            EO="SO"
        Name = str(adep)+"-"+str(dest)
        
        # 查找航路
        route, found = self.find_route_by_dep_arr(adep, dest)
        if not found:
            reply = QMessageBox.question(self, "未找到航路", 
                                        f"未找到从{adep}到{dest}的路线,是否手动输入?",
                                        QMessageBox.Yes | QMessageBox.No)
            if reply == QMessageBox.Yes:
                route, ok = QInputDialog.getText(self, "手动输入航路", "请输入航路:")
                with open(self.csv_path,"a",encoding='utf-8') as file:
                    file.write('{},{},{},{},,,{},\n'.format(adep,dest,Name,EO,route))
                if not ok or not route:
                    return
            else:
                return
        remark = self.find_remarks_by_dep_arr(adep, dest)
        rte = self.tower_rte_input.text() or route
        
        # 生成输出
        output = f"PSEUDOPILOT:ALL\n"
        output += f"@N:{callsign}:2000:1:{pos}:{alt}:0:{hdg}:0\n"
        output += f"$FP{callsign}:*A:I:{typ}:420:{adep}:0000:0000:{rfl}:{dest}:00:00:0:0::/v/{remark}:{route}\n"
        output += f"$ROUTE:{rte}\n"
        output += f"DELAY:1:8\n"
        output += f"REQALT::{alt}\n"
        output += f"INITIALPSEUDOPILOT:{self.tower_ini_input.text()}\n"
        output += f"\n"
        
        self.tower_output.setPlainText(output)
        self.statusBar().showMessage("塔台航班计划生成完成")
        
    def save_to_file(self):
        file_path, _ = QFileDialog.getSaveFileName(self, "保存文件", "", "文本文件 (*.txt)")
        if file_path:
            try:
                with open(file_path, 'a', encoding='utf-8') as file:
                    file.write(self.output_text.toPlainText())
                QMessageBox.information(self, "成功", "文件已保存")
                self.statusBar().showMessage(f"文件已保存至: {file_path}")
            except Exception as e:
                QMessageBox.critical(self, "错误", f"保存文件时出错: {e}")
                self.statusBar().showMessage("文件保存失败")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    
    # 设置应用字体
    font = QFont("Microsoft YaHei", 9)
    app.setFont(font)
    
    window = FlightPlanGenerator()
    window.show()
    sys.exit(app.exec_())