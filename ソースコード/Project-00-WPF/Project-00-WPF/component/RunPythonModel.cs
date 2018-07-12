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
//            //実行した結果を取得
//            var python_result1 = string.Empty;

//            //スクリプトのランタイムオプション
//            Dictionary<string, object> options = new Dictionary<string, object>();
//#if DEBUG
//            //デバッグ実行の場合スクリプトもデバッグモードにする。
//            options["Debug"] = true;
//#endif
//            //オプションを指定してPythonのランタイムを作成する。
//            ScriptRuntime pyRuntime = Python.CreateRuntime(options);

//            //ScriptScopeの型は実行時に解決される。
//            //Pythonのソースを指定(空の場合は実行フォルダ内とする)
//            string pythonPath = Properties.System.Default.PythonFilePath;
//            if (pythonPath == string.Empty)
//            {
//                pythonPath = System.Reflection.Assembly.GetExecutingAssembly().Location;
//            }
//            dynamic py = pyRuntime.UseFile(pythonPath + pythonName);

//            //Pythonのコードに書かれているメソッドを呼び出す。
//            //戻り値の型は実行時に解決される。
//            dynamic PyClassObject = py.getObject();

//            //Pythonからの戻り値を使用して何らかの処理。
//            Console.WriteLine("{0},{1}", PyClassObject.placeCode, PyClassObject.year);

            //Pythonスクリプト実行エンジン
            ScriptEngine pse = Python.CreateEngine();

            //実行エンジンに渡す値を設定する
            ScriptScope scope = pse.CreateScope();

            //"Csharp_value"という変数名で、"Symfo"という値を渡す
            scope.SetVariable("Csharp_value", "True");

            //Pythonのソースを指定(空の場合は実行フォルダ内とする)
            string pythonPath = Properties.System.Default.PythonFilePath;
            if (pythonPath == string.Empty)
            {
                pythonPath = System.Reflection.Assembly.GetExecutingAssembly().Location;
            }
            ScriptSource source = pse.CreateScriptSourceFromFile(pythonPath + pythonName);

            //ソースを実行する
            source.Execute(scope);

            //実行した結果を取得
            var python_result1 = scope.GetVariable<string>("result");

            return python_result1;
        }
    }
}
