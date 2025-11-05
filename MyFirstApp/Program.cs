// See https://aka.ms/new-console-template for more information
Console.WriteLine("Hello, World!");
Console.WriteLine("Welcome to .NET learning!");
Console.WriteLine("Today is a great day to code!");

Console.Write("What is your name? ");
string name = Console.ReadLine();
Console.Write("What is your age: ");
string ageInput = Console.ReadLine();
int age = int.Parse(ageInput);
int birthYear = 2025 - age;

Console.WriteLine("Nice to meet you, " + name + "!");
Console.WriteLine("I know your Birth Year!! So, "+name+" Your BirthYear Is:" + birthYear);
