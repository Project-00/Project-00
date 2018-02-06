using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Project_00_WPF.common
{
    class CommonContext //基本情報クラス
    {
        //ログインID
        private string loginId = string.Empty;
        public void SetLoginId(string loginId)
        {
            this.loginId = loginId;
        }
        public string GetLoginId()
        {
            return loginId;
        }

        //ログインパスワード
        private string loginPassword = string.Empty;
        public void SetLoginPassword(string loginPassword)
        {
            this.loginPassword = loginPassword;
        }
        public string GetLoginPassword()
        {
            return loginPassword;
        }

        //メールアドレス
        private string mailAddress = string.Empty;
        public void SetMailAddress(string mailAddress)
        {
            this.mailAddress = mailAddress;
        }
        public string GetMailAddress()
        {
            return mailAddress;
        }



    }
}
