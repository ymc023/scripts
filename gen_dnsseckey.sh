function gen_dnssec_key()
{
if read -t 20  -p "输入需要生成的key名称（多个名称以逗号隔开如;ya,default）:" input
then
    for key in $input
    do 

       key_file=`dnssec-keygen -a HMAC-MD5 -b 512 -n USER $key`
       key_content=`cat "$key_file.key"|awk '{print $7}'` 

       echo "key '$key' {
       algorithm hmac-md5;
       secret '$key_content';
       };" >>/etc/named/viewkey.conf
    done
echo "key文件生成完成."
fi
}
