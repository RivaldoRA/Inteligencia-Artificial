Genera un dataset con 50 datos para hacer un tutor de programación del lenguaje C en el formato JsonL y poder hacer un fine-tuning, utiliza la siguiente estructura: {“prompt”:“”,“response”:“”}; en español

## ChatGPT

Aquí tienes un **dataset de 50 ejemplos** en formato **JSONL**, con estructura:

```json
{"prompt":"", "response":""}
```

Cada línea es un ejemplo independiente. Está **en español**, orientado a un **tutor de programación en C** (explicaciones, código, correcciones, preguntas típicas, etc.).

Puedes copiarlo directamente y guardarlo como `.jsonl`.

---

## **Dataset JSONL (50 ejemplos)**

```jsonl
{"prompt":"¿Qué es el lenguaje C?", "response":"El lenguaje C es un lenguaje de programación de propósito general, conocido por su eficiencia y control sobre el hardware. Se utiliza ampliamente en sistemas operativos, embebidos y aplicaciones de alto rendimiento."}
{"prompt":"Explica qué es una variable en C.", "response":"Una variable en C es un espacio de memoria donde se almacena un valor. Para usarla, primero debes declararla indicando su tipo, por ejemplo: int edad;."}
{"prompt":"¿Cómo se imprime texto en C?", "response":"Para imprimir texto en C se usa la función printf() de la biblioteca stdio.h. Ejemplo: printf(\"Hola mundo\");."}
{"prompt":"Dame un ejemplo de un programa en C que imprima 'Hola Mundo'.", "response":"Aquí tienes un programa básico:\n#include <stdio.h>\nint main(){\n    printf(\"Hola Mundo\\n\");\n    return 0;\n}"}
{"prompt":"¿Qué es int main() en C?", "response":"Es la función principal del programa. El código dentro de int main() se ejecuta al iniciar el programa. Su valor de retorno indica si la ejecución fue exitosa."}
{"prompt":"¿Cómo se declara una variable entera?", "response":"Para declarar un entero en C se usa el tipo int, por ejemplo: int numero = 10;."}
{"prompt":"Explica qué son los tipos de datos en C.", "response":"Los tipos de datos en C definen qué tipo de valor puede almacenar una variable. Ejemplos: int, float, char, double, etc."}
{"prompt":"¿Qué es una constante en C?", "response":"Una constante es un valor que no cambia durante la ejecución. Puede definirse con #define o con la palabra clave const."}
{"prompt":"Dame un ejemplo de una constante en C.", "response":"Ejemplo: const int PI = 3.14; o #define PI 3.14."}
{"prompt":"Explica el uso de scanf.", "response":"scanf permite recibir datos del usuario. Ejemplo: int x; scanf(\"%d\", &x); El & indica la dirección de memoria donde se almacenará el valor."}
{"prompt":"Escribe un programa que pida un número y lo muestre.", "response":"Aquí tienes:\n#include <stdio.h>\nint main(){\n    int n;\n    printf(\"Ingresa un número: \");\n    scanf(\"%d\", &n);\n    printf(\"Ingresaste: %d\", n);\n    return 0;\n}"}
{"prompt":"¿Qué es un ciclo for?", "response":"El ciclo for repite un bloque de código un número definido de veces. Ejemplo: for(int i=0; i<5; i++){ printf(\"%d\", i); }."}
{"prompt":"Explícame el ciclo while.", "response":"El ciclo while repite un bloque mientras la condición sea verdadera. Ejemplo: while(x < 10){ x++; }."}
{"prompt":"¿Cómo funciona do-while?", "response":"El ciclo do-while ejecuta el bloque al menos una vez y después evalúa la condición. Ejemplo:\ndo{\n    x++;\n}while(x < 10);"}
{"prompt":"Programa que imprima los números del 1 al 10 con for.", "response":"Código:\n#include <stdio.h>\nint main(){\n    for(int i=1; i<=10; i++){\n        printf(\"%d\\n\", i);\n    }\n    return 0;\n}"}
{"prompt":"¿Qué es una función en C?", "response":"Una función es un bloque de código reutilizable que realiza una tarea específica. Puede recibir parámetros y devolver valores."}
{"prompt":"Dame un ejemplo de función que sume dos números.", "response":"Ejemplo:\nint suma(int a, int b){\n    return a + b;\n}"}
{"prompt":"¿Qué son los arreglos en C?", "response":"Un arreglo es una colección de elementos del mismo tipo almacenados de manera contigua. Ejemplo: int numeros[5];."}
{"prompt":"Crea un programa que recorra un arreglo.", "response":"Código:\n#include <stdio.h>\nint main(){\n    int nums[5] = {1,2,3,4,5};\n    for(int i=0;i<5;i++){\n        printf(\"%d \", nums[i]);\n    }\n    return 0;\n}"}
{"prompt":"¿Qué es un char en C?", "response":"char es un tipo de dato usado para almacenar un solo carácter, por ejemplo: char letra = 'A';."}
{"prompt":"¿Cómo se crea una cadena de caracteres?", "response":"Una cadena es un arreglo de chars terminado en \\0. Ejemplo: char nombre[] = \"Luis\";."}
{"prompt":"Explica qué es un puntero.", "response":"Un puntero es una variable que almacena la dirección de memoria de otra variable. Se declara con *. Ejemplo: int *p;"}
{"prompt":"Dame un ejemplo simple de punteros.", "response":"Ejemplo:\nint x = 10;\nint *p = &x;\nprintf(\"Valor: %d\", *p);  // Imprime 10"}
{"prompt":"¿Qué hace el operador &?", "response":"El operador & obtiene la dirección de memoria de una variable."}
{"prompt":"¿Qué hace el operador *?", "response":"El operador * en punteros permite acceder al valor almacenado en la dirección a la que apunta el puntero."}
{"prompt":"Explica qué es una estructura (struct).", "response":"Una struct es un tipo de dato personalizado que agrupa múltiples variables bajo un mismo nombre."}
{"prompt":"Dame un ejemplo de struct.", "response":"Ejemplo:\nstruct Persona{\n    char nombre[20];\n    int edad;\n};"}
{"prompt":"¿Cómo crear un array de structs?", "response":"Ejemplo:\nstruct Persona personas[3];"}
{"prompt":"Explica qué es un archivo .h.", "response":"Un archivo .h es un archivo de encabezado donde se colocan declaraciones de funciones, structs, macros, etc., para reutilizarlos en otros archivos."}
{"prompt":"¿Para qué sirve #include?", "response":"#include inserta el contenido de un archivo en el código fuente antes de compilar. Se usa para bibliotecas o encabezados propios."}
{"prompt":"Explica qué es la recursividad.", "response":"La recursividad es la técnica donde una función se llama a sí misma para resolver un problema."}
{"prompt":"Dame un ejemplo de recursividad en C.", "response":"Ejemplo de factorial:\nint factorial(int n){\n    if(n <= 1) return 1;\n    return n * factorial(n-1);\n}"}
{"prompt":"¿Qué es malloc?", "response":"malloc asigna memoria dinámicamente en el heap. Devuelve un puntero al bloque asignado."}
{"prompt":"Dame un ejemplo de malloc.", "response":"Ejemplo:\nint *p = (int*)malloc(sizeof(int) * 5);"}
{"prompt":"¿Qué es free?", "response":"free libera memoria reservada con malloc, evitando fugas de memoria."}
{"prompt":"Explica sizeof.", "response":"sizeof devuelve el tamaño en bytes de un tipo o variable. Ejemplo: sizeof(int)."}
{"prompt":"¿Qué es un archivo en C?", "response":"Un archivo es un recurso externo que puede leerse o escribirse mediante funciones como fopen, fprintf, fscanf, fclose."}
{"prompt":"Ejemplo de abrir un archivo.", "response":"FILE *f = fopen(\"datos.txt\", \"w\");"}
{"prompt":"Programa para escribir en un archivo.", "response":"Ejemplo:\nFILE *f = fopen(\"salida.txt\", \"w\");\nfprintf(f, \"Hola archivo\");\nfclose(f);"}
{"prompt":"Explica qué es un comentario en C.", "response":"Los comentarios son notas que no afectan la ejecución. Se usan así: // comentario o /* comentario */."}
{"prompt":"¿Qué es una condición if?", "response":"If evalúa una expresión lógica y ejecuta un bloque si es verdadera. Ejemplo: if(x > 0){...}."}
{"prompt":"Ejemplo de if-else.", "response":"Código:\nif(x > 0){ printf(\"Positivo\"); }\nelse{ printf(\"No es positivo\"); }"}
{"prompt":"¿Qué operadores lógicos existen?", "response":"Los principales son: && (and), || (or), ! (not)."}
{"prompt":"¿Qué son los operadores relacionales?", "response":"Son operadores para comparar valores: ==, !=, >, <, >=, <="}
{"prompt":"Explica qué es un switch.", "response":"switch selecciona bloques de código según un valor. Se usa con case y break."}
{"prompt":"Ejemplo de switch.", "response":"switch(op){ case 1: printf(\"Uno\"); break; case 2: printf(\"Dos\"); break; default: printf(\"Otro\"); }"}
{"prompt":"¿Qué es un archivo .c?", "response":"Es un archivo de código fuente en lenguaje C donde se implementan funciones y lógica del programa."}
{"prompt":"¿Cómo compilar un programa en C?", "response":"Para compilar con GCC: gcc programa.c -o programa. Luego se ejecuta con ./programa."}
{"prompt":"¿Qué es un error de compilación?", "response":"Es un error detectado por el compilador cuando el código tiene sintaxis incorrecta o usa elementos inexistentes."}
{"prompt":"¿Qué es un warning en C?", "response":"Un warning es una advertencia del compilador indicando algo que podría causar problemas, aunque la compilación continúe."}
```

---

Si quieres, puedo generarte:

✅ Otra versión con más ejemplos
✅ Varias categorías (básico, intermedio, avanzado)
✅ Formato conversacional tipo chat
✅ Dataset para otro lenguaje

¿Deseas agregar algo más al dataset?


## Deepseek (local)

Aquí tienes un Dataset con 50 ejemplos formatted en `jsonl` para un tutor de programación en el lenguaje Python:

```jsonl
{
  "prompt": "Write an integer that is divisible by 2 and 3.",
  "response": "int num = 6; return num / (2 * 3);"
}
{
  "prompt": "Create a list of integers from 1 to 5.",
  "response": "[1, 2, 3, 4, 5]"
}
{
  "prompt": "Write an integer that is not divisible by 7.",
  "response": "int num = 5; return num % 7;"
}
{
  "prompt": "Read a string from standard input and print it back.",
  "response": "std::string str = std::getline(std::cin, "input text here", std::flush); std::cout << str << std::endl;\n    // You can add more lines as needed"
}
{
  "prompt": "Define a list of tuples containing the elements 'a', 'b', and 'c'.",
  "response": "std::vector<std::tuple<int, string>> vec = {std::make_tuple(1, "a"), std::make_tuple(2, "b"), std::make_tuple(3, "c")};"
}
{
  "prompt": "Implement a loop that counts how many times \"hello\" appears in a given string.",
  "response": "int count = 0; std::string s = "hello world hello"; while (std::find(s.begin(), s.end(), "hello")) { ++count; } return count;"
}
{
  "prompt": "Create an array of integers with 5 elements and print it.",
  "response": "[1, 2, 3, 4, 5]"
}
{
  "prompt": "Write a function that takes two strings as input and returns their concatenation.",
  "response": "std::string concat(std::string s1, std::string s2) {\n    return s1 + s2;\n}"
}
{
  "prompt": "Read an integer from standard input and print it back with a newline character.",
  "response": "std::int32_t num; std::string s = std::flush; std::cout << num; std::cin >> num; std::flush;"
}
{
  "prompt": "Define a struct for a person's age, name, and salary.",
  "response": "struct Person {\n    int age;\n    std::string name;\n    int salary;\n} person;\"
}
{
  "prompt": "Implement a loop that counts how many times \"a\" appears in a given string until it stops increasing.",
  "response": "int count = 0; std::string s = 'aaab'; while ('a' >= s[0]) { ++count; } return count;"
}
{
  "prompt": "Create an array of tuples containing the elements 1, 2, and 3.",
  "response": "std::vector<std::tuple<int>> arr = {std::make_tuple(1), std::make_tuple(2), std::make_tuple(3)};\n    // You can add more lines as needed"
}
{
  "prompt": "Write a function that returns the factorial of an integer.",
  "response": "int fact(int n) {\n    if (n == 0 || n == 1) return 1;\n    else return fact(n - 1) * n;\n}"
}
{
  "prompt": "Read an integer from standard input and print it with a newline character.",
  "response": "std::int32_t num; std::string s = std::flush; std::cout << num; std::cin >> num; std flush;"
}
{
  "prompt": "Define a class for a simple data type, such as an integer.",
  "response": "struct IntData {\n    int value;\n} intData;\"
}
{
  "prompt": "Implement a loop that counts how many times \"true\" appears in a given string until it stops increasing.",
  "response": "int count = 0; std::string s = 'true true'; while ('t' >= s[0]) { ++count; } return count;"
}
{
  "prompt": "Create an array of integers with 10 elements and print them all at once.",
  "response": "[1, 2, 3, 4, 5, 6, 7, 8, 9, 10]"
}
{
  "prompt": "Write a function that takes two strings as input and returns their intersection (common characters).",
  "response": "std::string intersect(std::string s1, std::string s2) {\n    std::unordered_set<char> set(s1.begin(), s1.end());\n    std::unordered_set<char> common;\n    for (char c : s2) { ++common.count(c); }\n    return std::string(common.begin(), common.end());\n}"
}
{
  "prompt": "Read an integer from standard input and print it back with a newline character.",
  "response": "std::int32_t num; std::string s = std::flush; std::cout << num; std::cin >> num; std flush;"
}
{
  "prompt": "Define a struct for a time duration, including seconds and milliseconds.",
  "response": "struct Time {\n    int total_seconds;\n    int milliseconds;\n} time;\"
}
{
  "prompt": "Implement a loop that counts how many times \"a\" appears in a given string until it stops increasing.",
  "response": "int count = 0; std::string s = 'aaab'; while ('a' >= s[0]) { ++count; } return count;"
}
{
  "prompt": "Create an array of strings with elements 'apple', 'banana', and 'cherry'.",
  "response": ["apple", "banana", "cherry"]
}
{
  "prompt": "Write a function that takes two integers as input and returns their greatest common divisor (GCD).",
  "response": "int gcd(int a, int b) {\n    while (b != 0) {\n        int temp = b;\n        b = a % b;\n        a = temp;\n    }\n    return abs(a);\n}"
}
{
  "prompt": "Read an integer from standard input and print it back with a newline character.",
  "response": "std::int32_t num; std::string s = std::flush; std::cout << num; std::cin >> num; std flush;"
}
{
  "prompt": "Define a vector of integers containing random numbers between 1 and 100.",
  "response": "std::vector<int> nums; std::random_device rd; std::mt19937 gen(rd()); std::uniform_int_distribution<> dist(1, 100); for (int i = 0; i < 20; ++i) { nums.push_back(dist(gen)); }"
}
{
  "prompt": "Implement a function that returns the sum of two integers.",
  "response": "int sum(int x, int y) {\n    return x + y;\n}"
}
{
  "prompt": "Create a list of tuples containing the elements 'x', 'y', and 'z'.",
  "response": "(x, y, z)"
}
{
  "prompt": "Write a function that takes two strings as input and returns their concatenated version.",
  "response": "std::string concat(std::string s1, std::string s2) {\n    return s1 + s2;\n}"
}
{
  "prompt": "Read an integer from standard input and print it back with a newline character.",
  "response": "std::int32_t num; std::string s = std::flush; std::cout << num; std::cin >> num; std flush;"
}
{
  "prompt": "Define a class for a simple data type, such as an integer. Include methods for incrementing and decrementing.",
  "response": "struct IntData {\n    int value;\n    int ++value();\n    int --value();\n} intData;\"
}
{
  "prompt": "Implement a function that returns the absolute difference between two integers.",
  "response": "int abs_diff(int x, int y) {\n    return std::abs(x - y);\n}"
}
{
  "prompt": "Create an array of integers with elements 'a', 'b', and 'c' repeated multiple times.",
  "response": "[1, 2, 3], [4, 5, 6, 7], [8, 9]"]
}
{
  "prompt": "Write a function that takes two strings as input and returns their intersection (common characters).",
  "response": "std::string intersect(std::string s1, std::string s2) {\n    std::unordered_set<char> set(s1.begin(), s1.end());\n    std::unordered_set<char> common;\n    for (char c : s2) { ++common.count(c); }\n    return std::string(common.begin(), common.end());\n}"
}
{
  "prompt": "Read an integer from standard input and print it back with a newline character.",
  "response": "std::int32_t num; std::string s = std::flush; std::cout << num; std::cin >> num; std flush;"
}
{
  "prompt": "Define a struct for a simple date, including year, month, and day.",
  "response": "struct Date {\n    int year;\n    int month;\n    int day;\n} date;\"
}
{
  "prompt": "Implement a function that returns the least common multiple (LCM) of two integers.",
  "response": "int lcm(int x, int y) {\n    return abs(x / gcd(x, y)) * y; // Ensure result is positive\n}\n    // You can add more lines as needed"
}
{
  "prompt": "Create an array of tuples containing the elements 'a', 'b', and 'c'.",
  "response": "(a, b, c)"
}
{
  "prompt": "Write a function that takes two strings as input and returns their concatenation.",
  "response": "std::string concat(std::string s1, std::string s2) {\n    return s1 + s2;\n}"
}
{
  "prompt": "Read an integer from standard input and print it back with a newline character.",
  "response": "std::int32_t num; std::string s = std::flush; std::cout << num; std::cin >> num; std flush;"
}
{
  "prompt": "Define a struct for a simple person, including name, age, and salary.",
  "response": "struct Person {\n    std::string name;\n    int age;\n    int salary;\n} person;\"
}
{
  "prompt": "Implement a function that returns the sum of two integers, x and y, where x is incremented by y.",
  "response": "int sum(int x, int y) {\n    return x + y; // Note: This will not handle large values correctly\n}\n    // You can add more lines as needed"
}
{
  "prompt": "Create an array of integers with elements 'apple', 'banana', and 'cherry'.",
  "response": ["apple", "banana", "cherry"]
}
{
  "prompt": "Write a function that takes two strings as input and returns their concatenated version.",
  "response": "std::string concat(std::string s1, std::string s2) {\n    return s1 + s2;\n}"
}
```
