using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Project_00_WPF.component
{
    class RunPythonModel //Python実行クラス
    {
        public void Run(string path)
        {
            //スクリプトのランタイムオプション
            Dictionary<string, object> options = new Dictionary<string, object>();
            //デバッグ実行の場合スクリプトもデバッグモードにする。
            options["Debug"] = true;
            //オプションを指定してPythonのランタイムを作成する。
            ScriptRuntime pyRuntime = Python.CreateRuntime(options);

            //Pythonのファイルを指定する。
            //ScriptScopeの型は実行時に解決される。
            dynamic py = pyRuntime.UseFile(path);

            //Pythonのコードに書かれているメソッドを呼び出す。
            //戻り値の型は実行時に解決される。
            dynamic PyClassObject = py.getObject();

            //Pythonからの戻り値を使用して何らかの処理。
            Console.WriteLine("{0},{1}", PyClassObject.placeCode, PyClassObject.year);
        }
    }
}
