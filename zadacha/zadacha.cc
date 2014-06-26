#include<stdio.h>
#include <stdlib.h>

int main(int argc,char* argv[]){
	int sum=0;
	int now;
	int add=atoi(argv[1]);
	int dayMax=atoi(argv[2]);
	for(int i=1;i<=dayMax;i++){
		now=add*i;
		if(now>=dayMax && now%dayMax==0){
			sum++;
		}
	}
	printf("%d\n",sum);
	int dayMax2=dayMax;
	int add2=add;
	while(dayMax!=add){
		if(dayMax>add){
			dayMax-=add;
		} else {
			add-=dayMax;
		}
	}

	printf("%d\n",add);
	return 0;
}
