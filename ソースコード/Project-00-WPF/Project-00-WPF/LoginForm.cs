using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;

namespace Project_00_WPF
{
    public partial class LoginForm : Form
    {
        public LoginForm()
        {
            InitializeComponent();
        }

        #region 初期処理
        private void LoginForm_Load(object sender, EventArgs e)
        {
            //初期化処理
            //// マウス移動イベントを追加
            this.MouseDown += new MouseEventHandler(Form_MouseDown);
            this.MouseMove += new MouseEventHandler(Form_MouseMove);

            //エンターキーを割り当てる
            this.AcceptButton = this.LoginButton;

        }
        #endregion

        #region ×ボタン押下処理
        private void CloseButton_Click(object sender, EventArgs e)
        {
            //アプリケーションを終了する
            Application.Exit();
        }
        #endregion

        #region ログインボタン押下処理
        private void LoginButton_Click(object sender, EventArgs e)
        {
            Boolean setFlg = true;
            //ログインIDをセット
            if(LoginIdText.Text == string.Empty)
            {
                //値が入っていない場合は赤表示
                LoginIdText.BackColor = Color.PaleVioletRed;
                setFlg = false;
            }
            else{
                //値が入っている場合は通常表示
                LoginIdText.BackColor = Color.White;
            }

            //パスワードをセット
            if (LoginPasswordText.Text == string.Empty)
            {
                //値が入っていない場合は赤表示
                LoginPasswordText.BackColor = Color.PaleVioletRed;
                setFlg = false;
            }
            else
            {
                //値が入っている場合は通常表示
                LoginPasswordText.BackColor = Color.White;
            }

            if (setFlg)
            {
                Program.context.SetLoginId(LoginIdText.Text);
                Program.context.SetLoginPassword(LoginPasswordText.Text);
                //破棄する
                this.Dispose();
            }
        }
        #endregion

        #region フォーム操作
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
