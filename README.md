# 加密混淆JavaScript程序识别

作为恶意JavaScript文件的重要标志和攻击者常用的逃避检测手段之一，加密混淆的识别对于网络安全防护的加强有着重要的意义。本程序由Python 2编写的，用于识别加密混淆JavaScript程序。主程序输入为需要识别的文件的地址，以及一个JavaScriptKeywords文件（有提供），输出一个布尔值代表是否有加密混淆的情况存在。目前经过优化，可以达到识别准确率99%以上，误报率1%以下。

```
本文件依据Markdown格式编写，有条件请使用Markdown获得最佳的阅读体验
```

## 环境依赖

Python 2
Jupyter

## 部署准备

运行/修改此项目需要安装下面的Python库：
numpy
matplotlib
pandas
Scipy
Scikit-learn
```
pip install matplotlib
pip install pandas
pip install scikit-learn
```

## 使用方法

```Python
from DecideEncryptionObfuscation import predict_obfuscation
predict_obfuscation('路径', '关键字路径')
```

## 目录结构描述

|—— README.md                           // 说明文档  
|—— 程序                                // Python程序  
|   |—— DecideEncryptionObfuscation.py  // 主程序  
|   |—— ModeAnalysisRestructured.py  
|   |—— LexicalProcessing.py  
|   |—— GenerateModel.py  
|   |—— get_vector.py  
|   |—— Tesing.py                       // 各程序的调试程序  
|   └── PlotResults.py                  // 对于各个模式进行可视化处理  
|—— 文档  
|   |—— 模式总结.docx                    // 模式说明文件  
|   └── 加密混淆识别程序.pptx  
|—— 测试数据  
|   |—— Virus                           // 加密混淆文件  
|   |—— NormalProgrammes                // 正常文件  
|   └── Experiment Data                 // 模式测试文件  
└── 资料  
    |—— 基础知识                         // 词法分析、语法分析原理  
    |—— 论文                            // 有用的论文  
