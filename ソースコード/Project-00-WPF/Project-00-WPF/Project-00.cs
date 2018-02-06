using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;
//基本情報クラス
using Project_00_WPF.common;

namespace Project_00_WPF
{
    public partial class Project00 : Form
    {
        public Project00()
        {
            InitializeComponent();
        }

        #region 初期処理
        private void Project00_Load(object sender, EventArgs e)
        {
            //基本情報の取得
            //CommonContext context = new CommonContext();

            //// マウス移動イベントを追加
            this.MouseDown += new MouseEventHandler(Form_MouseDown);
            this.MouseMove += new MouseEventHandler(Form_MouseMove);

            //ログイン情報のチェック
            if (!LoginCheck(Program.context))
            {
                //ログインフォームをモーダルフォームとして表示する
                LoginForm loginForm = new LoginForm();
                loginForm.ShowDialog();

            }
        }
        #endregion

        #region 最小化ボタン押下処理
        private void MinimizedButton_Click(object sender, EventArgs e)
        {
            //最小化状態にする
            this.WindowState = FormWindowState.Minimized;
        }
        #endregion

        #region ×ボタン押下時処理
        private void CloseButton_Click(object sender, EventArgs e)
        {
            //アプリケーションを終了する
            Application.Exit();
        }

        //ログインチェック
        private Boolean LoginCheck(CommonContext context)
        {
            Boolean loginCheck = false;

            if (context.GetLoginId() != string.Empty & context.GetLoginPassword() != string.Empty)
            {
                loginCheck = true;
            }

            return loginCheck;
        }
        #endregion

        #region フォーム操作
        //フォーム操作
        // マウスポインタの位置を保存する
        private Point mousePoint;

        //マウスのボタンが押されたとき
        private void Form_MouseDown(object sender, MouseEventArgs e)
        {
            if ((e.Button & MouseButtons.Left) == MouseButtons.Left)
            {
                //位置を記憶する
                mousePoint = new Point(e.X, e.Y);
            }
        }

        //マウスが動いたとき
        private void Form_MouseMove(object sender, MouseEventArgs e)
        {
            if ((e.Button & MouseButtons.Left) == MouseButtons.Left)
            {
                this.Left += e.X - mousePoint.X;
                this.Top += e.Y - mousePoint.Y;
            }
        }
        #endregion

    }
}
