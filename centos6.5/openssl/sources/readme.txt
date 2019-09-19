编译方法：
1.上传并解压缩“openssl-fips-2.0.16.tar.gz”，执行以下命令编译、安装fips
	cd openssl-fips-2.0.16
	./config shared
	make
	make install
2.上传“openssl-1.0.2t-58.el6.src.rpm”，执行rpmbuild重新编译即可

注：
1.“openssl-1.0.2t-58.el6.src.rpm”看包含的“openssl-1.0.2t.tar.gz”包是修改过的包，并非原始包。
2.实际上，这个方案并不好，升级时会提示旧的openssl被其它库依赖，如果强行升级，opensshd会无法工作（无法远程连接），
会出现“/usr/lib64/libcrypto.so.10: no version information available”这样的错误。
这个错误是升级了 openssl 之后，依赖 openssl 的相关程序没有升级导致，openssl 严格要求运行的动态库版本和编译时 link 的版本要一致。
因此，并不建议使用此方案，留下这个仅作为将来的参考。

