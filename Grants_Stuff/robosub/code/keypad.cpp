
//as function: string input = keypad(); //loop until input
 
String keypad()
{
	String input = " ";

	 //col
	 write(5, low);
	 write(6, low);
	 write(13, low);
	 write(19, low);

	 //row
	 write(26, low);
	 write(12, low);
	 write(16, low);
	 write(20, low);

	//check col 5
	write(5, high);
	if(read(26))
	{	input = "*";
		break;
	}else if(read(12)){
		input = "7";
		break;
	}else if(read(16)){
		input = "4";
		break;
	}else if(read(20)){
		input = "1";
		break;	
	}
	write(5, low);
	write(6, high);
	if(read(26))
	{	input = "0";
		break;
	}else if(read(12)){
		input = "8";
		break;
	}else if(read(16)){
		input = "5";
		break;
	}else if(read(20)){
		input = "2";
		break;	
	}
	write(6, low);
	write(13, high);
	if(read(26))
	{	input = "#";
		break;
	}else if(read(12)){
		input = "9";
		break;
	}else if(read(16)){
		input = "6";
		break;
	}else if(read(20)){
		input = "3";
		break;	
	}
	write(13, low);
	write(19, high);
	if(read(26))
	{	input = "D";
		break;
	}else if(read(12)){
		input = "C";
		break;
	}else if(read(16)){
		input = "B";
		break;
	}else if(read(20)){
		input = "A";
		break;	
	}
	write(19, low);

	return input;
}
