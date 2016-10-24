# micro_assembler_Isabel_II

 Proyecto de Arquitectura de Computadoras
                              Curso 2014-15
  
                                 ISABEL-2
  
  
  Introducción
  ============
  
  Isabel-2 es una arquitectura de 16 bits.  El procesador tiene 16 registros de
  16 bits, nombrados R0 a R14, de propósito general, y SP (en la posición de R15)
  que actúa como puntero de la pila (stack pointer).
  
  Con registros de 16 bits, Isabel-2 es capaz de utilizar hasta 64Kb de RAM.
  
  Las instrucciones de Isabel-2 tienen longitud constante de 32 bits.
  
  La tabla siguiente muestra el juego de instrucciones, y su codificación.  Los 6
  primeros bits son el opcode. Luego vienen tres grupos de 4 bits para los
  registros RD (registro de destino), RA y RB. Los últimos 16 bits son para los
  valores constantes (K).
  
  Note que K y RB comparten dos bits. Naturalmente, ninguna instrucción usa a la
  vez a K y a RB. Los puntos representan bits que no se utilizan durante la
  interpretación de una instrucción.
  
  Mnemónico           Codificación
  ---------           -----------------------------------
  
                      OpCode  RD   RA   RB  
                      012345 7890 1234 5678 
                                                K
                                         7890123456789012
  
  NOP                 000000 .... .... ..................
  MOV RD,K            000001 xxxx .... ..xxxxxxxxxxxxxxxx
  MOV RD,RA           000010 xxxx xxxx ..................
  MOV RD,[K]          000011 xxxx .... ..xxxxxxxxxxxxxxxx
  MOV RD,[RA]         000100 xxxx xxxx ..................
  MOV [RA],K          000101 .... xxxx ..xxxxxxxxxxxxxxxx
  MOV [RA],RB         000110 .... xxxx xxxx..............
  MOV [K],RA          000111 .... xxxx ..xxxxxxxxxxxxxxxx
  PUSH RA             001000 .... xxxx ..................
  POP RD              001001 xxxx .... ..................
  CALL K              001010 .... .... ..xxxxxxxxxxxxxxxx
  CALL RA             001011 .... xxxx ..................
  RET                 001100 .... .... ..................
  JMP K               001101 .... .... ..xxxxxxxxxxxxxxxx
  JMP RA              001110 .... xxxx ..................
  JZ K                010000 .... .... ..xxxxxxxxxxxxxxxx
  JN K                010001 .... .... ..xxxxxxxxxxxxxxxx
  JE K                010010 .... .... ..xxxxxxxxxxxxxxxx
  JNE K               010011 .... .... ..xxxxxxxxxxxxxxxx
  JGT K               010100 .... .... ..xxxxxxxxxxxxxxxx
  JGE K               010101 .... .... ..xxxxxxxxxxxxxxxx
  JLT K               010110 .... .... ..xxxxxxxxxxxxxxxx
  JLE K               010111 .... .... ..xxxxxxxxxxxxxxxx
  TTY RA              011000 .... xxxx ..................
  TTY K               011001 .... .... ..xxxxxxxxxxxxxxxx
  KBD R1              011010 xxxx .... ..................
  ADD RD,RA,K         100000 xxxx xxxx ..xxxxxxxxxxxxxxxx
  ADD RD,RA,RB        100001 xxxx xxxx xxxx..............
  SUB RD,RA,K         100010 xxxx xxxx ..xxxxxxxxxxxxxxxx
  SUB RD,RA,RB        100011 xxxx xxxx xxxx..............
  MUL RD,RA,K         100100 xxxx xxxx ..xxxxxxxxxxxxxxxx
  MUL RD,RA,RB        100101 xxxx xxxx xxxx..............
  DIV RD,RA,K         100110 xxxx xxxx ..xxxxxxxxxxxxxxxx
  DIV RD,RA,RB        100111 xxxx xxxx xxxx..............
  MOD RD,RA,K         101000 xxxx xxxx ..xxxxxxxxxxxxxxxx
  MOD RD,RA,RB        101001 xxxx xxxx xxxx..............
  AND RD,RA,K         101010 xxxx xxxx ..xxxxxxxxxxxxxxxx
  AND RD,RA,RB        101011 xxxx xxxx xxxx..............
  OR RD,RA,K          101100 xxxx xxxx ..xxxxxxxxxxxxxxxx
  OR RD,RA,RB         101101 xxxx xxxx xxxx..............
  XOR RD,RA,K         101110 xxxx xxxx ..xxxxxxxxxxxxxxxx
  XOR RD,RA,RB        101111 xxxx xxxx xxxx..............
  SHL RD,K            110000 xxxx .... ..xxxxxxxxxxxxxxxx
  SHL RD,RA           110001 xxxx xxxx ..................
  ROL RD,K            110010 xxxx .... ..xxxxxxxxxxxxxxxx
  ROL RD,RA           110011 xxxx xxxx ..................
  CMP RA,K            110100 .... xxxx ..xxxxxxxxxxxxxxxx
  CMP RA,RB           110101 .... xxxx xxxx..............
  NEG RD,RA           110110 xxxx xxxx ..................
  NOT RD,RA           110111 xxxx xxxx ..................
  RND RD              111000 xxxx .... ..................
  HALT                111100 .... .... ..................
  
  El procesador debe implementarse como el módulo ISABEL-2 del circuito
  Isabel 2 Board que se brinda.
  
  Instrucciones
  =============
  
  NOP
  ---
      La instrucción NOP no hace nada. Tiene OpCode 000000 e ignora el resto de los bits.
  
      Codificación:
          000000 .... .... ..................
  
  
  MOV RD,K            
  --------
      Mueve el valor constante K al registro indicado.
  
      Codificación:
          000001 xxxx .... ..xxxxxxxxxxxxxxxx
  
      Ejemplos:
          MOV R1, 5    =>  000001 0001 0000 000000000000000101
          MOV R12, -1  =>  000001 1100 0000 001111111111111111    
  
  MOV RD,RA
  ---------
      Mueve el valor del registro RA hacia el registro RD.
  
      Codificación:
          000010 xxxx xxxx ..................
  
      Ejemplos:
          MOV R1,R7  =>  000010 0001 0111 000000000000000000
          MOV SP,R1  =>  000010 1111 0001 000000000000000000
  
      Note cómo SP es equivalente a R15.
  
  MOV RD,[K]
  ----------
      Mueve hacia el registro RD el valor de 16 bits almacenado
      en la RAM en la dirección constante K.
  
      Codificación:
          000011 xxxx .... ..xxxxxxxxxxxxxxxx
  
      Ejemplos:
          MOV R3,[6]  =>  000011 0011 0000 000000000000000110
          MOV R9,[0]  =>  000011 1001 0000 000000000000000000
  
  MOV RD,[RA]
  ----------
      Mueve hacia el registro RD el valor de 16 bits almacenado
      en la RAM en la dirección correspondiente al valor
      del registro RA.
  
      Codificación:
          000100 xxxx xxxx ..................
  
      Ejemplos:
          MOV R3,[R4]   =>  000100 0011 0100 000000000000000000
          MOV R9,[R10]  =>  000100 1001 1010 000000000000000000
  
  MOV [RA],K
  ----------
      Almacena el valor constante K en  la dirección de memoria
      correspondiente al valor del registro RA.
  
      Codificación:
          000101 .... xxxx ..xxxxxxxxxxxxxxxx
  
      Ejemplos:
          MOV [R1],  4  =>  000101 0000 0001 000000000000000100
          MOV [R1], -1  =>  000101 0000 0001 001111111111111111
  
  MOV [RA],RB
  -----------
      Almacena el valor del registro RB en la dirección de memoria
      correspondiente al valor del registro RA.
  
      Codificación:
          000110 .... xxxx xxxx..............
  
      Ejemplos:
          MOV [R1], R2  =>  000110 0000 0001 001000000000000000
          MOV [R9], SP  =>  000110 0000 1001 111100000000000000
  
      Note que RD no se usa y que los dos últimos bits de RB
      coinciden con los dos primeros bits que usaría K en
      otras instrucciones.
  
  MOV [K],RA
  ----------
      Almacena el valor del registro RA en la dirección de memoria
      correspondiente al valor constante K.
  
      Codificación:
          000111 .... xxxx ..xxxxxxxxxxxxxxxx
  
      Ejemplos:
          Similares a los de la instrucción MOV [RA],K pero con
          el opcode 000111.
  
  PUSH RA
  -------
      Esta instrucción almacena en el tope de la pila el valor del
      registro RA. La pila es simplemente el lugar de la memoria
      al que señala el registro SP. Después de hacer PUSH, el valor
      de SP se decrementa en 2. Es un convenio común que la pila
      "crezca hacia abajo". O sea, que SP empiece en un valor alto
      y vaya decreciendo con cada PUSH y creciendo con cada POP.
      Como los registros son de 16 bits, SP cambia de 2 en 2 con
      cada PUSH y POP. Esta instrucción sería equivalente,
      pero más rápida, que:
  
          SUB SP,SP,2     <= Decrementa SP en 2
          MOV [SP],RA     <= Guarda RA en RAM[SP]
  
      Codificación:
          001000 .... xxxx ..................
  
      Ejemplo:
          PUSH R9  =>  001000 0000 1001 000000000000000000
  
  POP RD
  ------
      Esta instrucción almacena en RD el valor que está en el tope
      de la pila y lo "expulsa". Realmente, basta con incrementar
      SP en 2. Es equivalente, pero más rápida, que:
  
          MOV RD,[SP]
          ADD SP,SP,2
  
      Codificación:
          001001 xxxx .... ..................
  
      Ejemplo:
          POP R9  =>  001001 1001 0000 000000000000000000
  
  CALL K
  ------
      Esta instrucción se utiliza para "llamar" a una subrutina.  Internamente,
      hace push del valor actual del Program Counter en la pila y "salta" a la
      dirección absoluta K. Saltar es almacenar K en el Program Counter.
  
      Esta instrucción no se puede imitar con otras instrucciones por dos
      motivos: el Program Counter no es accesible desde el ISA y las demás
      instrucciones de salto (ver más abajo) saltan a direcciones relativas al
      Program Counter.
  
      Codificación:
          001010 .... .... ..xxxxxxxxxxxxxxxx
  
      Ejemplo:
          CALL 1026  =>  001010 0000 0000 000000010000000010
  
  CALL RA
  -------
      Esta instrucción es equivalente a CALL K, pero usa el valor de RA
      como destino del salto.
  
      Codificación:
          001011 .... xxxx ..................
  
  RET
  ---
      Esta instrucción "retorna" de una subrutina. 
  
      La combinación de CALL y RET permite "llamar" subrutinas y retornar al punto
      desde el que se llamaron. Debe tenerse en cuenta que en alguna de las dos
      instrucciones el valor de PC tiene que crecer en 4, para que el programa
      continúe en la instrucción que sigue a CALL. Si ninguna de las dos modifica a
      PC, la ejecución de RET restaurará el valor que tenía PC al ejecutar CALL y la
      próxima instrucción que se ejecutará será precisamente CALL, provocando que la
      misma función se llame una y otra vez indefinidamente.
  
      Es equivalente almacenar PC + 4 en CALL y restaurarlo en RET, que almacenar PC
      en CALL y sumarle 4 en el RET. Lo importante es que tras un RET se ejecute la
      instrucción que sigue a CALL.
  
      Codificación:
          001100 .... .... ..................
  
  JMP K
  -----
      Esta instrucción hace un salto incondicional a la dirección relativa K.
      Relativo significa que el valor de K se suma al del Program Counter:
  
          PC = PC + K
  
      Esto permite saltar tanto hacia delante como hacia atrás. El bit de signo,
      no obstante, limita los saltos al rango -32768..32767, que no es una
      gran limitación, vale decir.
  
      Codificación:
          001101 .... .... ..xxxxxxxxxxxxxxxx
  
  JMP RA
  ------
      Equivalente a JMP K, pero la distancia saltada es el valor almacenado
      en el registro RA. Equivalente a:
  
          PC = PC + Registros[RA]
  
      Codificación:
          001110 .... xxxx ..................
  
  JZ K, JN K
  ----------
      Estas instrucciones son saltos condicionales al valor constante K, que se
      toma relativo al Program Counter.  O sea, si la condición se cumple, el salto
      es equivalente al de JMP K.
  
      La condición la determina la última operación aritmética o lógica realizada
      (excepto una comparación hecha con CMP).
  
      Si R fue el resultado de dicha operación, las condiciones son las
      siguientes:
  
          JZ      =>      R es cero (0).
          JN      =>      R es negativo (<0)
  
      Codificación:
          JZ K  =>  010000 .... .... ..xxxxxxxxxxxxxxxx
          JN K  =>  010001 .... .... ..xxxxxxxxxxxxxxxx
  
  {JE,JNE,JGT,JGE,JLT,JLE} K
  ---------------------------
      Estas instrucciones son equivalentes a JZ y JN, pero la condición
      la determina únicamente la última instrucción CMP que se realizó.
      Las demás instrucciones aritméticas no afectan el resultado de
      estas instrucciones de salto condicional.
  
      Si la última comparación fue CMP A,B las condiciones son
      las siguientes:
  
          JE  K  =>  A == B
          JNE K  =>  A != B
          JGT K  =>  A  > B
          JGE K  =>  A >= B
          JLT K  =>  A  < B
          JLE K  =>  A <= B
  
      Codificación:
          JE  K  =>  010010 .... .... ..xxxxxxxxxxxxxxxx
          JNE K  =>  010011 .... .... ..xxxxxxxxxxxxxxxx
          JGT K  =>  010100 .... .... ..xxxxxxxxxxxxxxxx
          JGE K  =>  010101 .... .... ..xxxxxxxxxxxxxxxx
          JLT K  =>  010110 .... .... ..xxxxxxxxxxxxxxxx
          JLE K  =>  010111 .... .... ..xxxxxxxxxxxxxxxx
  
  TTY RA
  ------
      Esta instrucción se utiliza para enviar un caracter a la pantalla
      conectada al procesador (TTY). La pantalla es un circuito síncrono.
      Para enviar un caracter, se ponen los 7 bits menos significativos
      de RA en la salida TTY DATA del procesador, se activa la salida
      TTY ENABLE y en el próximo ciclo la pantalla mostrará el caracter
      ASCII correspondiente a los 7 bits de TTY DATA.
  
      Codificación:
          011000 .... xxxx ..................
  
  TTY K
  -----
      Equivalente a TTY RA, pero con una constante.
  
      Codificación:
          011001 .... .... ..xxxxxxxxxxxxxxxx
  
  KBD R1
  ------
      Esta instrucción lee un caracter del teclado y lo almacena en R1.
      La entrada KBD AVAILABLE del procesador indica si hay algún caracter
      esperando en el buffer del teclado y la entrada KBD DATA, es un número
      de 7 bits que corresponde al código ASCII del caracter que está en
      la punta del buffer. El buffer del teclado funciona como una cola.
      Los caracteres se añaden a la cola cuando se teclea.
      En cada ciclo de reloj, si KBD ENABLE está activa, el teclado elimina
      el caracter que está en la punta de la cola.
  
      Si en el momento que esta instrucción se ejecuta, KBD AVAILABLE está
      desactivada, en R1 se almacena el valor -1.
  
      Codificación:
          011010 xxxx .... ..................
  
  ADD, SUB, MUL, DIV, MOD, AND, OR, XOR
  -------------------------------------
      Estas instrucciones realizan la operación aritmética o lógica
      correspondiente. Siempre tienen tres argumentos y hacen:
  
          Reg[RD] = Reg[RA] operación K  o
          Reg[RD] = Reg[RA] operación Reg[RB]
  
      Codificación:
  
          ADD RD,RA,K   =>  100000 xxxx xxxx ..xxxxxxxxxxxxxxxx
          ADD RD,RA,RB  =>  100001 xxxx xxxx xxxx..............
          SUB RD,RA,K   =>  100010 xxxx xxxx ..xxxxxxxxxxxxxxxx
          SUB RD,RA,RB  =>  100011 xxxx xxxx xxxx..............
          MUL RD,RA,K   =>  100100 xxxx xxxx ..xxxxxxxxxxxxxxxx
          MUL RD,RA,RB  =>  100101 xxxx xxxx xxxx..............
          DIV RD,RA,K   =>  100110 xxxx xxxx ..xxxxxxxxxxxxxxxx
          DIV RD,RA,RB  =>  100111 xxxx xxxx xxxx..............
          MOD RD,RA,K   =>  101000 xxxx xxxx ..xxxxxxxxxxxxxxxx
          MOD RD,RA,RB  =>  101001 xxxx xxxx xxxx..............
          AND RD,RA,K   =>  101010 xxxx xxxx ..xxxxxxxxxxxxxxxx
          AND RD,RA,RB  =>  101011 xxxx xxxx xxxx..............
          OR RD,RA,K    =>  101100 xxxx xxxx ..xxxxxxxxxxxxxxxx
          OR RD,RA,RB   =>  101101 xxxx xxxx xxxx..............
          XOR RD,RA,K   =>  101110 xxxx xxxx ..xxxxxxxxxxxxxxxx
          XOR RD,RA,RB  =>  101111 xxxx xxxx xxxx..............
  
  SHL RD,K
  SHL RD,RA
  ---------
      Estas instrucciónes modifican el registro RD haciendo un
      desplazamiento de bits. Si K o Reg[RA] es positivo,
      el desplazamiento es hacia la izquierda. Si K o Reg[RA]
      es negativo, el desplazamiento es hacia la derecha.
  
      Codificación:
  
          SHL RD,K   =>  110000 xxxx .... ..xxxxxxxxxxxxxxxx
          SHL RD,RA  =>  110001 xxxx xxxx ..................
  
      Nota: Logisim tiene dos componentes separados para
      desplazar a la izquierda y la derecha. Es necesario
      añadir la lógica necesaria para seleccionar la operación
      correcta.
  
  ROL RD,K 
  ROL RD,RA
  ---------
      Similares a SHL, estas instrucciones modifican el registro
      RD haciendo una rotación. Al igual que con SHL, el signo
      del segundo argumento determina si la rotación es hacia
      la izquierda o hacia la derecha.
  
      Logisim tiene la operación de rotación como una modalidad
      de la componente aritmética Shifter.
  
      Codificación:
  
          ROL RD,K   =>  110010 xxxx .... ..xxxxxxxxxxxxxxxx
          ROL RD,RA  =>  110011 xxxx xxxx ..................
  
  
  CMP RA,K 
  CMP RA,RB
  ---------
      Esta instrucción no modifica ningún registro. Solamente
      compara sus argumentos y establece algún estado interno
      del procesador que determinará el resultado de las
      instrucciones de salto condicional JE, JNE, JGT, JGE,
      JLT y JLE. Ver arriba cómo se interpreta.
  
      Esta instrucción no afecta los saltos JZ y JN.
  
      Codificación:
  
          CMP RA,K   =>  110100 .... xxxx ..xxxxxxxxxxxxxxxx
          CMP RA,RB  =>  110101 .... xxxx xxxx..............
  
  
  NEG RD,RA
  ---------
      Esta instrucción almacena en el registro RD el opuesto
      aritmético del valor del registro RA (el complemento
      a 2). Por ejemplo, tras:
  
          MOV R2, 8
          NEG R1, R2
  
      el registro R2 tendrá el valor 1111111111111000 (-8)
  
      Codificación:
          110110 xxxx xxxx ..................
  
  NOT RD,RA
  ---------
      Esta instrucción almacena en RD opuesto lógico de RA,
      o sea, su negación bit a bit, o complemento a 1.
      Por ejemplo, tras:
  
          MOV R2,8
          NOT R1,R2
  
      el registro R1 tendrá el valor 1111111111110111 (-9).
  
      Codificación:
          110111 xxxx xxxx ..................
  
  RND RD
  ------
      Esta instrucción almacena en RD un número aleatorio.
  
      Codificación:
          111000 xxxx .... ..................
  
  HALT
  ----
      Esta instrucción activa la salida STOP del procesador
      que detiene su ejecución. Es imprescindible para detener
      la simulación durante la verificación del proyecto.
  
      Codificación:
          111100 .... .... ..................
  
  
  Program Counter
  ===============
  
  El valor del Program Counter (PC) representa la dirección de memoria de la
  próxima instrucción que se va a ejecutar. Como en ISABEL-2 las instrucciones
  ocupan 4 bytes, cada vez que el procesador ejecuta una instrucción que no sea
  de salto el valor de PC aumenta en 4.
  
  Las instrucciones de salto relativo (JMP, JZ, JN, ...) suman su argumento al de
  PC. Si el valor del Program Counter no es un múltiplo de 4, el procesador puede
  simplemente interpretarlo como si fuera el múltiplo de 4 más cercano por
  debajo.
  
  Como resultado de esto, si un programa quisiera saltarse una instrucción, debe
  hacer un salto con argumento 8:
  
      MOV R3,1
      CMP R1,R2
      JGT 8
      MOV R3,0
  
  Esto es como decir, en C o C++, R3 = (R1 > R2)? 1 : 0. Otros resultados de este
  comportamiento son que JMP 4 es lo mismo que NOP y JMP 0 es un ciclo infinito.
  
  
  Acceso a la memoria
  ===================
  
  La memoria, para el programador de Isabel-2, es un array plano de 64KB,
  direccionable a nivel de 1 bytes. Sin embargo, las transferencias entre
  la RAM y el procesador ocurren siempre en bloques de 2 bytes (16 bits).
  
  El procesador puede ignorar cualquier dirección de memoria que sea impar,
  e interpretarla como si fuera el número par más cercano por debajo. O sea
  "MOV R1, [0]" y "MOV R1, [1]" hacen lo mismo.
  
  Si un programa hace:
  
      MOV R1, [0]
  
  al registro R1 se copiarán los bytes 0 y 1 de la RAM. 
  
  Isabel es una arquitectura Little-Endian, que significa que, en cada
  palabra de 16 bits, el byte con dirección más pequeña es el menos significativo
  y el de dirección más grande es el más significativo. Esto luce "al revés"
  de cómo se escriben normalmente los números.
  
  Supongamos que los primeros bytes de la RAM tienen estos valores:
  
         0     1     2     3     4     5 
      --------------------------------------
      |  1  |  2  |  1  |  2  |  1  |  2  | ...
      --------------------------------------
  
  Al hacer
  
      MOV R1, [0]
  
  el byte 0 de la RAM, que tiene el valor 1 va hacia la parte menos
  significative de R1 y el byte 1, con valor 2, va hacia la más significativa.
  El valor final de R1 sería 2 * 256 + 1 = 513
  
  Las escrituras se comportan de igual forma. Si se hace:
  
      MOV [0], 1027
  
  se escribirán para el byte 0 de la RAM la parte menos significativa del
  valor 1027 y para el byte 1 la parte más significativa.
  
  1027 es 00000100 00000011 en binario. El byte más significativo es 4
  y el menos significativo es 3 (1024 = 256 * 4 + 3). Así que la memoria
  quedaría así:
  
         0     1     2     3     4     5 
      --------------------------------------
      |  3  |  4  |  1  |  2  |  1  |  2  | ...
      --------------------------------------
  
  Interfaz con la memoria
  =======================
  
  El módulo RAM del circuito IsabelBoard implementa una memoria asíncrona de
  64KB. Esta memoria está organizada en 8192 bloques de 8 bytes. Esta RAM es más
  lenta que el procesador, y le toma varios ciclos leer y escribir datos. La
  cantidad de ciclos que toma hacer una lectura o una escritura están,
  respectivamente, en las salidas constantes RT (Read Time) y WT (Write Time).
  
  (Aunque estas salidas sean constantes, no se deben usar sus valores "a mano"
  dentro del CPU. Hay que obtenerlos de la RAM.  Los profesores vamos a probar
  distintas combinaciones de esos valores durante la verificación del procesador
  y este debe comportarse en concordancia.)
  
  Como la RAM tiene 8192 bloques, su entrada ADDR es de 13 bits.  Después de
  pasados RT ciclos de CPU de establecerse esa entrada, si la entrada CS (Chip
  Select) está en 1 y la entrada ¬R/W está en 0, la RAM proporcina los 8 bytes
  del bloque seleccionado mediante las 4 salidas de 16 bits O0, O1, O2 y O3.
  
  Análogamente, hay 4 entradas de 16 bits, I0, I1, I2 e I3, por las que se envían
  a la RAM valores para ser escritos en la dirección ADDR. Sin embargo, la
  escritura puede hacerse parcialmente, usando la entrada MASK.
  
  La RAM está dividida en 4 bancos que actúan como columnas o slices.  Cada
  bloque de 8 bytes de la RAM por tanto está dividido en 4 palabras de 2 bytes
  (16 bits). Los primeros 32 bytes de la RAM lucen así:
  
  
     Banco 0  Banco 1  Banco 2  Banco 3
     -------  -------  -------  -------
      00 01    02 03    04 05    06 07    <-- Bloque 0
      08 09    10 11    12 13    14 15    <-- Bloque 1
      16 17    18 19    20 21    22 23    <-- Bloque 2
      24 25    26 27    28 29    30 31    <-- Bloque 3
        .        .        .        .            .
        .        .        .        .            .
        .        .        .        .            .
  
  
  La entrada MASK es una entrada de 4 bits que selecciona cuál o cuales bancos
  van a ser modificados por una operación de escritura.  El bit menos
  significativo de MASK selecciona el Banco 0, el más significativo selecciona el
  Banco 3.
  
  Por ejemplo, si la entrada MASK tiene el valor 8 (en binario 1000) y la entrada
  ADDR es 0, la escritura solo afectaría los bytes 6 y 7 de la RAM, pues estos
  están en el bloque 0 y en el banco 3.  En esos dos bytes se escribiría el valor
  de la entrada I3.
  
  Si la entrada MASK fuera 12 y ADDR fuera 2 (en binario 1100), la escritura
  modificaría los bytes 20, 21, 22 y 23 (bloque 2, bancos 2 y 3).  En esos 4
  bytes se escribirían los valores de las entradas I2 e I3.
  
  Las entrada MASK no afecta las operaciones de lectura. Las salidas O0 a O3
  siempre contienen el bloque completo solicitado en ADDR.
  
  Las escrituras se realizan cuando CS es 1 y ¬R/W es 1 y toman la cantidad de
  ciclos de CPU que indica la salida WT.
  
  
  Ensamblaje
  ==========
  
  El archivo .zip al final de esta página contiene el ensamblador de Isabel-2, ISAIAS. Es un
  programa que convierte un archivo de texto con código mnemónico de Isabel-2 en
  cuatro imágenes para los bancos de la RAM con las instrucciones codificadas.
  
  El ensamblador entiende además una pseudoinstrucción DATA que permite insertar
  valores directos en la salida ensamblada, y etiquetas para los saltos, con
  esta forma:
  
      # ciclo hasta que R1 sea 0
      label1:
          SUB R1,R1,1
          JZ :label2
          JMP :label1
      label2:
          MOV ...
  
  El carácter '#' se puede usar para insertar comentarios en el código.
  
  (ISAIAS = ISAbel Incredible ASsembler). 
  
  Verificación
  ============
  
  Pronto estará disponible un verificador online para los procesadores.
  
  
  Costo y Presupuesto
  ===================
  
  El procesador va a tener un presupuesto. Cada componente utilizada tendrá un
  costo asociado y el costo total del procesador no podrá exceder el presupuesto.
  Los costos específicos de cada componente serán publicados pronto. El
  verificador online del procesador tendrá la facilidad de calcular el costo
  total de un procesador.
  
  Al final del proyecto, se entregarán premios a los procesadores con mejor
  relación costo/velocidad.
  
  Evaluación
  ==========
  
  El proyecto debe realizarse en equipos de no más de dos (2) estudiantes. El
  plazo para entregar los proyectos es el viernes 15 de mayo de 2015. Después de
  la entrega, se realizará una revisión oral con un profesor y los miembros de
  cada equipo. Se puede entregar y revisarse en cualquier momento antes de la
  expiración del plazo.
  
  
  Historial
  =========
  
    2015-05-06
    ----------
  
    - Se corregió la especificación de PUSH: el acceso a la RAM y la
      modificación de SP estaban al revés.
  
    - Se añadió una sección sobre el Program Counter
  
    - Se simplificó el acceso a la memoria, las direcciones impares se
      interpretan como la dirección par más cercana por debajo.
  
    - Se eliminó la sección que explicaba cómo se manejaban las direcciones
      impares.
  
    - Ya está público un ensamblador.
  
    - Se añadió el historial.
  
    2015-05-07
    ----------
  
    - Se corregió la especificación de RET y CALL. Alguna debe incrementar
      PC en 4.
  
    - Se acutalizó el assembler a Python2/Python3, se le añadieron labels,
      la pseudoinstrucción DATA, un directorio opcional de salida si se le
      pasa un 2do argumento y se renombró a ISAIAS.

