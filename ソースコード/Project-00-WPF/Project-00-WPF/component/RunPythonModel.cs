using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.IO;
using System.Diagnostics;
using IronPython.Hosting;
using Microsoft.Scripting.Hosting;

namespace Project_00_WPF.component
{
    public static class RunPythonModel //Python実行クラス
    {
        public static string Run(string pythonName)
        {
            //Pythonスクリプト実行エンジン
            ScriptEngine pse = Python.CreateEngine();

            //実行エンジンに渡す値を設定する
            ScriptScope scope = pse.CreateScope();

            //"Csharp_value"という変数名で、"Symfo"という値を渡す
            scope.SetVariable("Csharp_value", "Symfo");

            //Pythonのソースを指定(空の場合は実行フォルダ内とする)
            string pythonPath = Properties.System.Default.PythonFilePath;
            if (pythonPath == string.Empty)
            {
                pythonPath = System.Reflection.Assembly.GetExecutingAssembly().Location;
            }
            ScriptSource source = pse.CreateScriptSourceFromFile(pythonPath + pythonName);

            //C:\sample.pyにおいたソースを実行する
            source.Execute(scope);

            //実行した結果を取得
            var python_result1 = scope.GetVariable<string>("python_result");

            return python_result1;
        }
    }
}
