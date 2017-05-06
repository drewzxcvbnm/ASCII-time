#include <cstring>
#include <iostream>
#include <ctime>
using namespace std;

void print(char t1[])
{
	cout<<string(750,'\b');
	int digit;
	static const char num[11][21]={"### # # # # # # ### "," #  ##   #   #  ### ","###   # ### #   ### ","###   #  ##   # ### ",\
	"# # # # ###   #   # ","### #   ###   # ### ","### #   ### # # ### ","###   #  ##   #   # ",\
	"### # # ### # # ### ","### # # ###   # ### ","     #       #      "};
	for(int l=0;l<5;l++)
	{
		for(size_t i=0;i<strlen(t1);i++)
		{
			if(t1[i]==':'){digit=10;}
			else{digit=t1[i]-'0';}
			if(l==0){for(int j=0;j<4;j++) cout<<num[digit][j];}
			if(l==1){for(int j=4;j<8;j++) cout<<num[digit][j];}
			if(l==2){for(int j=8;j<12;j++) cout<<num[digit][j];}
			if(l==3){for(int j=12;j<16;j++) cout<<num[digit][j];}
			if(l==4){for(int j=16;j<20;j++) cout<<num[digit][j];}
		}
		cout<<endl;
	}
}

int main()
{
	cout<<"\n\n\n\n\n\n";
	char t1[128],t2[128];
	time_t tm;
	struct tm *timeinfo;
	time(&tm);
	timeinfo=localtime(&tm);
	while(true)
	{
		strftime(t1,128,"%T",timeinfo);
		print(t1);
		while(true)
		{
			time(&tm);
			timeinfo=localtime(&tm);
			strftime(t2,128,"%T",timeinfo);
			if(strcmp(t1,t2)!=0){break;}
			struct timespec tm;tm.tv_sec=1;
			nanosleep(&tm,NULL);
		}
		
	}
	return 0;
}
