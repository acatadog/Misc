���뷽����
1.�ϴ�����ѹ����openssl-fips-2.0.16.tar.gz����ִ������������롢��װfips
	cd openssl-fips-2.0.16
	./config shared
	make
	make install
2.�ϴ���openssl-1.0.2t-58.el6.src.rpm����ִ��rpmbuild���±��뼴��

ע��
1.��openssl-1.0.2t-58.el6.src.rpm���������ġ�openssl-1.0.2t.tar.gz�������޸Ĺ��İ�������ԭʼ����
2.ʵ���ϣ�������������ã�����ʱ����ʾ�ɵ�openssl�����������������ǿ��������opensshd���޷��������޷�Զ�����ӣ���
����֡�/usr/lib64/libcrypto.so.10: no version information available�������Ĵ���
��������������� openssl ֮������ openssl ����س���û���������£�openssl �ϸ�Ҫ�����еĶ�̬��汾�ͱ���ʱ link �İ汾Ҫһ�¡�
��ˣ���������ʹ�ô˷����������������Ϊ�����Ĳο���

