---
title: Advanced Types
category: concepts
book: programming-typescript
chapter: 6
tags: [typescript, advanced-types, variance, refinement, mapped-types, conditional-types, type-guards, nominal-types, generics]
created: 2026-05-30
updated: 2026-05-30
status: active
---

# Advanced Types

> 📍 **Programming TypeScript · Cap. 6** · [⬅ Cap. 5: Classes & Interfaces](./05-classes-and-interfaces.md) · [Cap. 7: Handling Errors ➡](./07-handling-errors.md) · [📚 KB Index](../../../README.md)

> **TL;DR** — El sistema de tipos de TypeScript es expresivo de manera no trivial: maneja **subtyping con variancia** (covariante en objetos/arrays/return-types, contravariante en parámetros de función), **refina tipos** según el control flow (`typeof`, `instanceof`, `in`, discriminated unions), garantiza **totalidad** (todos los casos cubiertos), te deja **operar sobre tipos** como si fueran datos (`keyof`, keying-in, `Record`, **mapped types**, **conditional types con `infer`**), te da **escape hatches** (`as`, `!`, definite assignment) cuando necesitás romper las reglas, y permite **simular tipos nominales** con type branding cuando la equivalencia estructural no alcanza.

---

## 📑 In this chapter

0. [🎓 For Dummies — empezá por acá](#for-dummies-empeza-por-aca)
1. [Relationships Between Types](#relationships-between-types)
   - Subtypes & Supertypes
   - Variance (la pieza clave)
   - Assignability
   - Type Widening
   - Refinement (control-flow type narrowing)
   - Totality (exhaustiveness)
2. [Advanced Object Types](#advanced-object-types)
   - Keying-in (`O[K]`) y `keyof`
   - `Record<K, V>`
   - Mapped Types
   - Companion Object Pattern
3. [Advanced Function Types](#advanced-function-types)
   - Mejor inferencia para tuples
   - User-Defined Type Guards (`x is T`)
   - Conditional Types (`T extends U ? A : B`)
   - Distributividad y `infer`
   - Built-in conditional types
4. [Escape Hatches](#escape-hatches)
   - Type Assertions (`as`)
   - Non-null Assertions (`!`)
   - Definite Assignment Assertions
5. [Simulating Nominal Types con type branding](#simulating-nominal-types)
6. [Safely Extending the Prototype](#safely-extending-the-prototype)
7. [⭐ Amplification: patrones y casos reales](#amplification)
8. [⚠️ Pitfalls](#pitfalls)
9. [Interview Tips](#interview-tips)
10. [Ejercicios del libro (con resoluciones)](#ejercicios)

---

## 🎓 For Dummies — empezá por acá

Imagina que el sistema de tipos de TypeScript es como un **portero muy paranoico** en la entrada de un edificio. Cada función, cada variable, cada propiedad es una puerta con un cartel: "solo paso si traes un `Bird`", "solo paso si traes un `string`", etc.

Hasta ahora aprendiste **lo básico**: si la puerta dice `string`, traés un string. Si dice `Bird`, traés un Bird. **Easy**.

**El capítulo 6 es lo que pasa cuando las puertas se complican.**

### 🔑 Las 6 ideas grandes (con analogía cotidiana)

| # | Concepto | Analogía cotidiana |
|---|----------|---------------------|
| 1 | **Variance** | Si el delivery te pide "un perro", podés mandar un caniche (subtipo). Pero si pide una función *que reciba perros*, no podés mandar una *que reciba solo caniches* — porque le podrías mandar un labrador y rompería. |
| 2 | **Refinement** | El portero se acuerda. Si en la entrada ya te chequeó "este es un string", adentro no te lo vuelve a pedir. Pero si la conversación cambia de tema, se olvida. |
| 3 | **Totality** | Si decís que tu función devuelve "un día de la semana" y solo manejás "Lunes", el compilador te grita: "¿y los otros 6?". |
| 4 | **Mapped types** | Una fotocopiadora con filtros. "Hacéme una copia de este objeto, pero con todos los campos marcados como opcionales". |
| 5 | **Conditional types** | Tipos con `if/else`. "Si T es un array, devolvéme el tipo de sus elementos. Si no, devolvéme T tal cual." |
| 6 | **Type branding** | Pintar dos billetes idénticos de colores distintos. Físicamente son lo mismo (ambos son `string`), pero el sistema te impide pagar en pesos con un billete que pintaste como "dólares". |

### El recorrido del capítulo, en una frase

> Empezás entendiendo **cómo se comparan** los tipos (variance), después aprendés a **operar sobre ellos** como si fueran datos (keyof, mapped, conditional), después aprendés cuándo **romper las reglas** sin morir en el intento (escape hatches), y terminás aprendiendo dos patrones avanzados (**nominal types** y **prototype extension**).

### ¿Por qué esto te sirve si venís de C# o Java?

C# tiene variance explícita (`out`/`in` en interfaces genéricas). TypeScript la hace **implícita** y aplica reglas distintas según el tipo (covariante en propiedades, contravariante en parámetros). Saber esto te ahorra **horas** de "¿por qué no compila esta función que parece estar bien?".

Mapped types y conditional types son cosas que **no existen** en C# / Java tradicional. Son una forma de hacer "programación a nivel de tipos" — escribir tipos que dependen de otros tipos. Esto es lo que hace que TypeScript pueda tipear cosas como Redux/Apollo/React props sin que vos tengas que escribir cada variante a mano.

¿Listo? ⬇️

---

## Relationships Between Types

### Subtypes & Supertypes

**Definición operativa:**

- **B es subtipo de A** (`B <: A`) si podés usar un B en **cualquier lugar** donde se espera un A.
- **B es supertipo de A** (`B >: A`) si podés usar un A en **cualquier lugar** donde se espera un B. (Es el reverso.)

### Ejemplos canónicos en TS

```typescript
// Array es subtipo de Object
let arr: object = [1, 2, 3];  // OK

// Tuple es subtipo de Array
let tup: number[] = [1, 2] as [number, number];  // OK

// Todo es subtipo de any → any es supertipo de todo
let x: any = "hola";   // OK
let y: any = 42;       // OK

// never es subtipo de todo → todo es supertipo de never
function fail(): never { throw new Error(); }
let z: number = fail();  // OK (nunca pasa, pero el tipo encaja)

// Bird extends Animal → Bird <: Animal
class Animal {}
class Bird extends Animal { chirp() {} }
let a: Animal = new Bird();  // OK
```

### Sintaxis pseudo-formal del libro

Para hablar más rápido, Cherny usa:

- `A <: B` = "A es subtipo (o igual) a B"
- `A >: B` = "A es supertipo (o igual) a B"

(No es sintaxis válida de TS, es **notación didáctica**.)

### Variance — la parte que parece magia pero no es

La pregunta clave: si `Bird <: Animal`, **¿qué pasa con `Array<Bird>` vs `Array<Animal>`?** ¿Y con funciones que reciben/devuelven `Bird` vs `Animal`?

Las 4 variancias posibles:

| Variance | Querés un T y te dejan pasar… | En TS aplica a… |
|----------|-------------------------------|------------------|
| **Invariance** | exactamente un T | en algunos lenguajes para mutables — TS no usa |
| **Covariance** | un T o cualquier subtipo (`<: T`) | objects, classes, arrays, **return types de funciones** |
| **Contravariance** | un T o cualquier supertipo (`>: T`) | **parámetros de funciones**, **`this` de funciones** |
| **Bivariance** | cualquiera de los dos | legacy default de TS (sin `strictFunctionTypes`) |

#### Covariance en shapes (objetos)

```typescript
type ExistingUser = { id: number, name: string };
type NewUser = { name: string };

function deleteUser(user: { id?: number, name: string }) {
  delete user.id;
}

let existingUser: ExistingUser = { id: 123, name: "Ima" };
deleteUser(existingUser);  // OK: ExistingUser <: {id?, name}
                           //    porque {id: number} <: {id?: number}
```

**¿Por qué OK?** Cada propiedad del shape que pasás es subtipo de la propiedad que se espera. Los **shapes son covariantes en sus propiedades**.

> ⚠️ Esto **no es del todo seguro** (¡el `delete` modifica el objeto y al volver, TS sigue creyendo que `id` existe!), pero TS prefiere ergonomía sobre paranoia.

#### Contravariance en parámetros de funciones — el famoso "¿por qué se da vuelta?"

Setup:

```typescript
class Animal {}
class Bird extends Animal { chirp() {} }
class Crow extends Bird { caw() {} }
// Crow <: Bird <: Animal
```

Función que recibe una función:

```typescript
function clone(f: (b: Bird) => Bird): void {
  let parent = new Bird();
  let babyBird = f(parent);     // (1) llama f con un Bird
  babyBird.chirp();             // (2) espera que el resultado sea al menos un Bird
}
```

¿Qué funciones podés pasarle a `clone`?

```typescript
clone((b: Bird) => new Bird());     // ✓ exacto
clone((b: Bird) => new Crow());     // ✓ Crow <: Bird (return covariante)
clone((b: Bird) => new Animal());   // ✗ Animal no es Bird (no podrías hacer .chirp())

clone((a: Animal) => new Bird());   // ✓ Animal es supertipo de Bird (param contravariante)
clone((c: Crow) => new Bird());     // ✗ y si clone le pasa un Bird que no es Crow? .caw() rompería
```

**La regla, formalizada:**

Una función A es subtipo de una función B (`A <: B`) si:

1. `A`'s `this` type es **`>: B`'s this type** (contravariante)
2. Cada parámetro de A es **`>: ` su parámetro correspondiente en B** (contravariante)
3. El return type de A es **`<: ` el return type de B** (covariante)

> 💡 **Regla mnemotécnica**: parámetros se "abren" (aceptan más), returns se "cierran" (devuelven menos pero más específico).

#### TSC Flag: `strictFunctionTypes`

Por motivos legacy, TS por default trata parámetros como **bivariantes**. Para activar el comportamiento seguro (contravariante):

```json
{ "compilerOptions": { "strictFunctionTypes": true } }
```

Está incluido en `"strict": true`.

### Assignability

> Reglas que TS sigue para decidir "¿es A asignable a B?".

**Para tipos no-enum** (arrays, booleans, numbers, objects, functions, classes, instances, strings, literales):

A es asignable a B si:
1. `A <: B`, **o**
2. A es `any`.

**Para enums:**

A es asignable a un enum B si:
1. A es miembro de B, **o**
2. B tiene al menos un miembro `number` y A es `number`.

> ⚠️ La regla 2 para enums es una fuente de bugs común. Cherny **recomienda evitar enums** y usar string literals + unions.

### Type Widening

> TS **infiere tipos lo más generales posibles** cuando declarás con `let`/`var`, y los más específicos con `const`. Esto se llama widening.

```typescript
let a = 'x';          // string (widened)
const b = 'x';        // 'x' (literal, no widened)

let c = 3;            // number
const d = 3;          // 3

let e = { x: 3 };     // { x: number }
const f = { x: 3 };   // { x: number } — ojo, miembros sí se ensanchan
```

**Para evitar widening con `let`:** anotación explícita.

```typescript
let g: 'x' = 'x';     // 'x'
let h: 3 = 3;         // 3
```

**Reasignar un tipo narrow a un `let`:** widening pasa.

```typescript
const a = 'x';        // 'x'
let b = a;            // string — ¡se ensanchó!

const c: 'x' = 'x';   // 'x'
let d = c;            // 'x' — porque la fuente ya tenía anotación
```

**`null` / `undefined` se widen a `any`** (salvo cuando dejan el scope con valor concreto):

```typescript
let a = null;         // any
a = 3;                // any

function x() {
  let a = null;       // any
  a = 3;
  return a;
}
x();                  // number — al salir del scope, TS le asigna tipo definitivo
```

#### El tipo `const` (`as const`)

Opt out de widening **e** marca todo como `readonly`, recursivamente.

```typescript
let a = { x: 3 };                 // { x: number }
let b = { x: 3 } as const;        // { readonly x: 3 }

let c = [1, { x: 2 }];            // (number | { x: number })[]
let d = [1, { x: 2 }] as const;   // readonly [1, { readonly x: 2 }]
```

> 💡 **Útil para**: configs de Redux actions, action types, opciones inmutables.

#### Excess Property Checking

Cuando pasás un **fresh object literal** a algo que espera un tipo concreto, TS te tira error si tenés propiedades que el destino no espera (atajo para detectar typos).

```typescript
type Options = { baseURL: string, tier?: 'prod' | 'dev' };

new API({
  baseURL: 'https://api.x.com',
  tierr: 'prod'    // ✗ Error: 'tierr' does not exist in type 'Options'. Did you mean 'tier'?
});
```

**Casos donde TS no chequea exceso** (el objeto deja de ser "fresh"):

```typescript
new API({ baseURL: 'x', badTier: 'y' } as Options);  // ✓ — type assertion saca freshness

let bad = { baseURL: 'x', badTier: 'y' };
new API(bad);  // ✓ — asignar a variable saca freshness

let opts: Options = { baseURL: 'x', badTier: 'y' };  // ✗ aquí sí chequea, en el assign
new API(opts);
```

### Refinement (control-flow-based type narrowing)

> TS lee tu código como un programador y **angosta** los tipos según los chequeos que hagas. A esto se le llama **flow-based type inference**.

Disparadores de refinamiento:

- `typeof`, `instanceof`, `in`
- comparaciones de igualdad / desigualdad
- truthy / falsy checks (`if (x)`, `x && ...`, `x || ...`)
- discriminated unions (ver abajo)

#### Ejemplo: parsear un width CSS

```typescript
type Unit = 'cm' | 'px' | '%';
let units: Unit[] = ['cm', 'px', '%'];

function parseUnit(value: string): Unit | null {
  for (let u of units) if (value.endsWith(u)) return u;
  return null;
}

type Width = { unit: Unit, value: number };

function parseWidth(width: number | string | null | undefined): Width | null {
  if (width == null) return null;                       // [1] descarta null y undefined
  if (typeof width === 'number')                         // [2] separa number
    return { unit: 'px', value: width };
  // [3] acá width: string (lo que queda)
  let unit = parseUnit(width);
  if (unit) return { unit, value: parseFloat(width) };   // [4] unit: Unit
  return null;
}
```

Pasos del refinamiento:

| Paso | Tipo de `width` después de la guard |
|------|-------------------------------------|
| Entrada | `number \| string \| null \| undefined` |
| Después de `if (width == null) return` | `number \| string` |
| Dentro de `if (typeof width === 'number')` | `number` |
| Después del `if (typeof === 'number')` (con return adentro) | `string` |

#### Discriminated Unions (tagged unions)

Cuando tu union son shapes con propiedades **que se solapan**, TS pierde el track. La solución: agregar un campo **discriminador** con tipo literal.

❌ Sin discriminator:

```typescript
type UserTextEvent = { value: string, target: HTMLInputElement };
type UserMouseEvent = { value: [number, number], target: HTMLElement };
type UserEvent = UserTextEvent | UserMouseEvent;

function handle(event: UserEvent) {
  if (typeof event.value === 'string') {
    event.target;  // HTMLInputElement | HTMLElement (!!! no refinó)
  }
}
```

✓ Con discriminator (`type` tag):

```typescript
type UserTextEvent  = { type: 'TextEvent',  value: string, target: HTMLInputElement };
type UserMouseEvent = { type: 'MouseEvent', value: [number, number], target: HTMLElement };
type UserEvent = UserTextEvent | UserMouseEvent;

function handle(event: UserEvent) {
  if (event.type === 'TextEvent') {
    event.value;   // string
    event.target;  // HTMLInputElement
  } else {
    event.value;   // [number, number]
    event.target;  // HTMLElement
  }
}
```

**Buen discriminador** = literal type, único, en la misma "key" en cada miembro, no genérico, mutuamente exclusivo.

> 💡 **Aplicación directa**: Redux/Flux actions, React `useReducer`, eventos de un EventEmitter, GraphQL union types.

### Totality (exhaustiveness checking)

> Pattern matching style: TS te avisa si te olvidaste de cubrir un caso.

```typescript
type Weekday = 'Mon' | 'Tue' | 'Wed' | 'Thu' | 'Fri';
type Day = Weekday | 'Sat' | 'Sun';

function getNextDay(w: Weekday): Day {
  switch (w) {
    case 'Mon': return 'Tue';
    // ✗ Error TS2366: Function lacks ending return statement
    //                and return type does not include 'undefined'.
  }
}
```

#### TSC Flag: `noImplicitReturns`

Activar `noImplicitReturns: true` en tsconfig fuerza que **todos los paths** de tus funciones devuelvan algo si declaran un return type.

#### Pattern: el `never` exhaustivo

Para forzar exhaustividad en un `switch`, agregás un default con `never`:

```typescript
function getNextDay(w: Weekday): Day {
  switch (w) {
    case 'Mon': return 'Tue';
    case 'Tue': return 'Wed';
    case 'Wed': return 'Thu';
    case 'Thu': return 'Fri';
    case 'Fri': return 'Sat';
    default:
      const _exhaustive: never = w;  // si agregás un día al type, esto rompe
      throw new Error(`Unhandled day: ${w}`);
  }
}
```

> 💡 **Patrón canónico** en Redux reducers para forzar manejo de todas las actions.

---

## Advanced Object Types

### Keying-in (`O[K]`) — busqueda de tipo por clave

> Como `obj[key]` en JS, pero a nivel de tipos.

```typescript
type APIResponse = {
  user: {
    userId: string,
    friendList: {
      count: number,
      friends: { firstName: string, lastName: string }[]
    }
  }
};

type FriendList = APIResponse['user']['friendList'];
// = { count: number, friends: {...}[] }

type Friend = FriendList['friends'][number];
// = { firstName: string, lastName: string }
//   ↑ usar 'number' para indexar arrays; para tuples usar 0, 1, etc.
```

> ⚠️ **Siempre con bracket notation (`['key']`), nunca con dot notation.**

### El operador `keyof`

> Devuelve la unión de literales tipo string que representan **todas las claves** de un objeto.

```typescript
type Response = APIResponse;
type ResponseKeys = keyof Response;                  // 'user'
type UserKeys = keyof Response['user'];              // 'userId' | 'friendList'
```

#### Combinando `keyof` + keying-in: un `get()` tipado

```typescript
function get<O extends object, K extends keyof O>(o: O, k: K): O[K] {
  return o[k];
}

let logged = get({ a: 1, b: 'x' }, 'a');  // number
let bad   = get({ a: 1, b: 'x' }, 'c');   // ✗ Error: 'c' no asignable a 'a' | 'b'
```

#### Versión con paths anidados (overloaded)

```typescript
type Get = {
  <O extends object, K1 extends keyof O>(o: O, k1: K1): O[K1];
  <O extends object, K1 extends keyof O, K2 extends keyof O[K1]>(o: O, k1: K1, k2: K2): O[K1][K2];
  <O extends object, K1 extends keyof O, K2 extends keyof O[K1], K3 extends keyof O[K1][K2]>
    (o: O, k1: K1, k2: K2, k3: K3): O[K1][K2][K3];
};

let get: Get = (obj: any, ...keys: string[]) =>
  keys.reduce((acc, k) => acc[k], obj);

let activityLog = {
  lastEvent: new Date(),
  events: [{ id: 'x', timestamp: new Date(), type: 'Read' as 'Read' | 'Write' }]
};
get(activityLog, 'events', 0, 'type');  // 'Read' | 'Write'
get(activityLog, 'bad');                 // ✗ Error
```

#### TSC Flag: `keyofStringsOnly`

Por default `keyof` en TS devuelve `string | number | symbol` (porque JS soporta keys symbol). Si querés el comportamiento legacy "solo strings", activá `keyofStringsOnly: true`.

### `Record<K, V>` — built-in mapped type

> Atajo para "objeto con claves de tipo K y valores de tipo V".

```typescript
type Weekday = 'Mon' | 'Tue' | 'Wed' | 'Thu' | 'Fri';
type Day = Weekday | 'Sat' | 'Sun';

let nextDay: Record<Weekday, Day> = {
  Mon: 'Tue'
  // ✗ Error: faltan Tue, Wed, Thu, Fri
};
```

A diferencia de un index signature (`{ [k: string]: V }`), **`Record` exige TODAS las claves**.

### Mapped Types

> "Para cada clave K en este conjunto, defíneme una propiedad de tipo V". Una **transformación sobre un tipo objeto**, hecha al nivel de tipos.

#### Sintaxis

```typescript
type MyMappedType = {
  [Key in UnionType]: ValueType
};
```

#### Ejemplo: día siguiente, exhaustivo

```typescript
let nextDay: { [K in Weekday]: Day } = {
  Mon: 'Tue'
  // ✗ Error: faltan Tue, Wed, Thu, Fri
};
```

#### El poder real: transformar tipos existentes

```typescript
type Account = {
  id: number,
  isEmployee: boolean,
  notes: string[]
};

// Hacer todo opcional
type OptionalAccount = { [K in keyof Account]?: Account[K] };

// Hacer todo nullable
type NullableAccount = { [K in keyof Account]: Account[K] | null };

// Hacer todo readonly
type ReadonlyAccount = { readonly [K in keyof Account]: Account[K] };

// REVERTIR readonly (con el "minus" operator)
type Writable<T> = { -readonly [K in keyof T]: T[K] };

// REVERTIR optional
type Required<T> = { [K in keyof T]-?: T[K] };
```

| Operador | Significado |
|----------|-------------|
| `?` | hacer opcional |
| `-?` | quitar optional |
| `readonly` (= `+readonly`) | hacer readonly |
| `-readonly` | quitar readonly |

#### Built-in mapped types (en `lib.es5.d.ts`)

| Type | Hace |
|------|------|
| `Record<K, V>` | objeto con claves K y valores V |
| `Partial<T>` | todas las propiedades opcionales |
| `Required<T>` | todas las propiedades requeridas |
| `Readonly<T>` | todas las propiedades readonly |
| `Pick<T, K>` | subtipo de T con solo las claves K |
| `Omit<T, K>` | subtipo de T sin las claves K (TS ≥ 3.5) |

### Companion Object Pattern

> Misma idea que en Scala: un **tipo** y un **valor** con el mismo nombre, conviviendo. En TS, **tipos y valores viven en namespaces separados**, entonces el mismo identificador puede ser ambos.

```typescript
// El tipo
type Currency = {
  unit: 'EUR' | 'GBP' | 'JPY' | 'USD',
  value: number
};

// El valor (objeto con utilidades sobre el tipo)
let Currency = {
  DEFAULT: 'USD' as const,
  from(value: number, unit: Currency['unit'] = 'USD'): Currency {
    return { unit, value };
  }
};

// Consumo
import { Currency } from './Currency';

let amountDue: Currency = { unit: 'JPY', value: 83733.10 };  // Currency como tipo
let other = Currency.from(330, 'EUR');                        // Currency como valor
```

> 💡 **Usalo cuando** un tipo y un objeto helper son semánticamente uno. Ejemplos: `Currency`, `DateRange`, `UserID`.

---

## Advanced Function Types

### Improving Type Inference for Tuples

TS por default infiere tipos amplios para arrays literales:

```typescript
let a = [1, true];  // (number | boolean)[]
```

Para forzar tuple inference (sin usar `as const`):

```typescript
function tuple<T extends unknown[]>(...ts: T): T {
  return ts;
}

let a = tuple(1, true);  // [number, boolean]
```

> Por qué funciona: cuando un parámetro genérico es **rest**, TS lo infiere como tuple en lugar de array.

### User-Defined Type Guards (`x is T`)

#### El problema

```typescript
function isString(a: unknown): boolean {
  return typeof a === 'string';
}

function parseInput(input: string | number) {
  if (isString(input)) {
    input.toUpperCase();  // ✗ Error TS2339: Property 'toUpperCase' does not exist on type 'number'.
  }
}
```

El refinamiento que `isString` hace internamente **se pierde al salir del scope**. Todo lo que TS sabe es "devolvió un boolean".

#### La solución: type predicate (`x is T`)

```typescript
function isString(a: unknown): a is string {
  return typeof a === 'string';
}

function parseInput(input: string | number) {
  if (isString(input)) {
    input.toUpperCase();  // ✓ — TS sabe que aquí input es string
  } else {
    input.toFixed(2);     // ✓ — TS sabe que aquí input es number
  }
}
```

Limitaciones: aplica a **un solo parámetro**. Pero puede ser sobre tipos complejos:

```typescript
type Dialog = LegacyDialog | ModernDialog;

function isLegacyDialog(d: Dialog): d is LegacyDialog {
  return 'oldStyle' in d;
}
```

### Conditional Types — la feature más distintiva de TS

> Tipos con `if/else`: `T extends U ? A : B`.

#### Ejemplo simple

```typescript
type IsString<T> = T extends string ? true : false;

type A = IsString<string>;   // true
type B = IsString<number>;   // false
```

Se pueden anidar como ternarios:

```typescript
type TypeName<T> =
  T extends string  ? 'string'  :
  T extends number  ? 'number'  :
  T extends boolean ? 'boolean' :
  T extends Function ? 'function' :
  'object';
```

#### Distributividad

> Cuando aplicás un conditional type a una **union**, TS la **distribuye**.

Regla: `(A | B | C) extends T ? X : Y` ≡ `(A extends T ? X : Y) | (B extends T ? X : Y) | (C extends T ? X : Y)`.

```typescript
type ToArray<T> = T[];
type A = ToArray<number | string>;       // (number | string)[]

type ToArray2<T> = T extends unknown ? T[] : T[];   // ¡el condicional fuerza distribución!
type B = ToArray2<number | string>;      // number[] | string[]
```

#### Caso real: `Without<T, U>`

> "Los tipos que están en T pero no en U".

```typescript
type Without<T, U> = T extends U ? never : T;

type A = Without<boolean | number | string, boolean>;  // number | string
```

Paso a paso:

1. `Without<boolean | number | string, boolean>`
2. Distribuye: `Without<boolean, boolean> | Without<number, boolean> | Without<string, boolean>`
3. Sustituye definición: `(boolean extends boolean ? never : boolean) | (number extends boolean ? never : number) | (string extends boolean ? never : string)`
4. Evalúa: `never | number | string`
5. Simplifica: `number | string` (porque `never` es identidad de la union)

> 💡 Sin distributividad terminarías con `never`. **La distributividad es lo que hace `Without` útil.**

#### El keyword `infer`

> Declara un type variable **inline dentro del condicional**. TS lo deduce del contexto.

```typescript
type ElementType<T> = T extends (infer U)[] ? U : T;

type A = ElementType<number[]>;        // number
type B = ElementType<string>;          // string (no era array)
```

Caso real: extraer el tipo del segundo argumento de una función.

```typescript
type SecondArg<F> = F extends (a: any, b: infer B) => any ? B : never;

type SliceSecond = SecondArg<typeof Array['prototype']['slice']>;  // number | undefined
```

> 💡 Sin `infer`, tendrías que declarar U como parámetro genérico de `ElementType`, lo que obliga al caller a pasarlo — perdiendo el sentido del wrapper.

#### Built-in conditional types

| Type | Hace |
|------|------|
| `Exclude<T, U>` | `Without<T, U>` — tipos de T no asignables a U |
| `Extract<T, U>` | inversa de Exclude: tipos de T sí asignables a U |
| `NonNullable<T>` | quita `null` y `undefined` |
| `ReturnType<F>` | tipo del return de F (no funciona bien con generics ni overloads) |
| `Parameters<F>` | tipo de los parameters de F (tuple) |
| `InstanceType<C>` | tipo de instancia de un constructor C |

```typescript
type Strs = Exclude<number | string, number>;            // string
type Nums = Extract<number | string, number>;            // number
type X = NonNullable<{ a?: number | null }['a']>;        // number
type R = ReturnType<(a: number) => string>;              // string
type I = InstanceType<{ new(): { b: number } }>;         // { b: number }
```

---

## Escape Hatches

> Cuando necesitás *romper* las reglas. Cherny es claro: **usalas lo menos posible**. Si te encontrás usándolas seguido, probablemente estás haciendo algo mal.

### Type Assertions (`as T`)

Le decís al compilador "confía en mí, esto es T".

```typescript
function formatInput(input: string) { /* ... */ }
function getUserInput(): string | number { /* ... */ return ""; }

let input = getUserInput();
formatInput(input as string);    // sintaxis preferida
formatInput(<string>input);      // sintaxis legacy — choca con TSX, evitar
```

**Solo podés assertir** un tipo a su **supertipo o subtipo**. Si dos tipos no se relacionan:

```typescript
let n: number = 5;
let s: string = n as string;        // ✗ Error
let s: string = (n as any) as string;  // ✓ (¡pero estás haciendo algo mal!)
```

### Non-null Assertions (`!`)

Para `T | null` o `T | null | undefined`, le decís "confía en mí, no es null/undefined".

```typescript
type Dialog = { id?: string };

function closeDialog(dialog: Dialog) {
  if (!dialog.id) return;

  setTimeout(() =>
    removeFromDOM(
      dialog,
      document.getElementById(dialog.id!)!   // dos asserts: dialog.id es string, getElementById no es null
    )
  );
}

function removeFromDOM(dialog: Dialog, element: Element) {
  element.parentNode!.removeChild(element);  // parentNode no es null
  delete dialog.id;
}
```

> 💡 **Si te encontrás usando muchos `!`**, refactorizá: en este caso, podrías partir `Dialog` en un union `VisibleDialog | DestroyedDialog`.

```typescript
type VisibleDialog = { id: string };
type DestroyedDialog = {};
type Dialog = VisibleDialog | DestroyedDialog;

function closeDialog(dialog: Dialog) {
  if (!('id' in dialog)) return;     // refinamiento → dialog: VisibleDialog
  setTimeout(() =>
    removeFromDOM(dialog, document.getElementById(dialog.id)!)
  );
}
```

### Definite Assignment Assertions (`let x!: T`)

Decís "voy a asignar esto antes de usarlo, te juro".

```typescript
let userId: string;
fetchUser();
userId.toUpperCase();  // ✗ Error TS2454: Variable 'userId' is used before being assigned.

function fetchUser() {
  userId = globalCache.get('userId');
}
```

Con definite assignment:

```typescript
let userId!: string;   // ← el bang
fetchUser();
userId.toUpperCase();  // ✓
```

> Igual que con non-null asserts: si lo usás seguido, hay olor a refactor.

---

## Simulating Nominal Types

> TS es **structural**: dos tipos con la misma forma son intercambiables. A veces querés **nominal**: distinguir por nombre aunque la forma sea igual.

### El problema

```typescript
type CompanyID = string;
type OrderID = string;
type UserID = string;
type ID = CompanyID | OrderID | UserID;

function queryForUser(id: UserID) { /* ... */ }

let companyId: CompanyID = 'b4843361';
queryForUser(companyId);   // ✓ — TS lo permite porque ambos son string
                            //     (¡pero semánticamente es un bug!)
```

### La solución: **type branding**

```typescript
type CompanyID = string & { readonly brand: unique symbol };
type OrderID   = string & { readonly brand: unique symbol };
type UserID    = string & { readonly brand: unique symbol };
type ID = CompanyID | OrderID | UserID;

function CompanyID(id: string) { return id as CompanyID; }
function OrderID(id: string)   { return id as OrderID; }
function UserID(id: string)    { return id as UserID; }

function queryForUser(id: UserID) { /* ... */ }

let companyId = CompanyID('8a6076cf');
let userId    = UserID('d21b1dbf');

queryForUser(userId);     // ✓
queryForUser(companyId);  // ✗ Error TS2345: Argument of type 'CompanyID'
                          //   is not assignable to parameter of type 'UserID'.
```

**¿Cómo funciona?** El intersection con `{ brand: unique symbol }` produce un tipo "imposible de construir naturalmente". `unique symbol` es uno de los pocos tipos nominales reales de TS (el otro es `enum`). La única manera de obtener un valor del tipo branded es **vía la function constructor** que hace la `as` assertion.

**Costo en runtime:** ninguno. El brand es puramente compile-time. Cada ID sigue siendo un `string` al ejecutar.

> 💡 **Aplicalo en**: IDs de dominio diferentes (UserID, OrderID), unidades de medida (Meters, Feet), strings con formato (Email, URL, SHA256), money con currency (USD, EUR).

---

## Safely Extending the Prototype

> Antes era pecado. Con TS, podés agregar métodos a prototipos built-in **de manera segura**.

Setup: queremos `[1,2,3].zip(['a','b','c'])` que devuelva `[[1,'a'],[2,'b'],[3,'c']]`.

```typescript
// zip.ts

interface Array<T> {                    // [1] augmenta la interface global Array
  zip<U>(list: U[]): [T, U][];
}

Array.prototype.zip = function<T, U>(    // [2] implementa el método
  this: T[],
  list: U[]
): [T, U][] {
  return this.map((v, k) => tuple(v, list[k]));
};
```

| Paso | Qué hace |
|------|----------|
| [1] | Declaration merging con la interface global `Array<T>` |
| [2] | Implementación; usa `this: T[]` para inferir T |
| `tuple()` | Helper para inferir tupla en lugar de `(T \| U)[]` (ver sección anterior) |

#### Si el archivo está en module mode

Si tu `zip.ts` tiene imports/exports, no está en script mode. Necesitás `declare global`:

```typescript
import { something } from 'somewhere';

declare global {
  interface Array<T> {
    zip<U>(list: U[]): [T, U][];
  }
}
```

#### Forzar import explícito

En `tsconfig.json`, excluí el archivo del compile:

```json
{ "exclude": ["./zip.ts"] }
```

Así, cualquier archivo que use `.zip` está obligado a hacer `import './zip'` primero — garantizando que el monkey-patch corra antes.

```typescript
import './zip';
[1, 2, 3].map(n => n * 2).zip(['a', 'b', 'c']);  // [number, string][]
```

---

## ⭐ Amplification

### Patrón: Redux reducer con discriminated union + exhaustive `never`

```typescript
type Action =
  | { type: 'ADD_TODO', text: string }
  | { type: 'REMOVE_TODO', id: number }
  | { type: 'TOGGLE_TODO', id: number };

function reducer(state: Todo[], action: Action): Todo[] {
  switch (action.type) {
    case 'ADD_TODO':
      return [...state, { id: Date.now(), text: action.text, done: false }];
    case 'REMOVE_TODO':
      return state.filter(t => t.id !== action.id);
    case 'TOGGLE_TODO':
      return state.map(t => t.id === action.id ? { ...t, done: !t.done } : t);
    default:
      const _exhaustive: never = action;   // si agregás una Action, esto rompe
      return state;
  }
}
```

### Patrón: API response typesafe con keying-in

```typescript
type Schema = {
  users: { id: string, name: string };
  posts: { id: string, title: string, body: string };
  comments: { id: string, postId: string, text: string };
};

function fetch<K extends keyof Schema>(resource: K): Promise<Schema[K]> {
  return fetch(`/api/${resource}`).then(r => r.json());
}

fetch('users');     // Promise<{ id: string, name: string }>
fetch('posts');     // Promise<{ id: string, title: string, body: string }>
fetch('reactions'); // ✗ — no existe en Schema
```

### Mapped + Conditional: `DeepPartial<T>`

```typescript
type DeepPartial<T> = {
  [K in keyof T]?: T[K] extends object ? DeepPartial<T[K]> : T[K];
};

type Config = {
  server: { host: string, port: number, ssl: { cert: string, key: string } };
  client: { timeout: number };
};

let override: DeepPartial<Config> = {
  server: { ssl: { cert: 'new' } }   // ✓ — todo opcional, hasta el fondo
};
```

### Type branding para validación de strings

```typescript
type Email = string & { readonly brand: unique symbol };

function parseEmail(s: string): Email | null {
  return /^[^\s@]+@[^\s@]+$/.test(s) ? (s as Email) : null;
}

function sendEmail(to: Email, body: string) { /* ... */ }

let raw = "user@example.com";
let email = parseEmail(raw);
if (email) sendEmail(email, "hi");
// sendEmail(raw, "hi"); ✗ — raw es string, no Email
```

---

## ⚠️ Pitfalls

| # | Pitfall | Cómo evitar |
|---|---------|-------------|
| 1 | Olvidar `strictFunctionTypes` y usar parámetros bivariantes (default legacy) | Usar `"strict": true` en tsconfig |
| 2 | Excess property checking se pierde al asignar a variable | Si necesitás el chequeo, pasá object literal directo |
| 3 | Refinamiento se pierde al cruzar function scope (arrow callbacks, async, setTimeout) | Asignar a `const` local antes del cruce |
| 4 | Tipo `any` se contagia silenciosamente | Activar `noImplicitAny` |
| 5 | Usar `as` para "callar al compilador" sin entender la causa | Buscar el shape real; usar `as unknown as T` como último recurso (señal de problema) |
| 6 | Definir conditional types sin distribución cuando la necesitás | Envolver con `[T] extends [U]` para **desactivar** distribución; usar `T extends U` para activarla |
| 7 | Usar `enum` esperando comportamiento de tipos seguros | Preferir `'a' \| 'b' \| 'c'` (string literal unions) |
| 8 | Modificar el prototipo sin garantizar que se importe primero | Excluir del compile y `import './zip'` explícito en cada uso |
| 9 | Type guards con bugs ("a is string" pero la implementación devuelve true para otros tipos) | Tests unitarios sobre los guards |
| 10 | Confiar en `ReturnType<F>` con funciones genéricas o overloaded | TS resuelve a la última signature; no siempre lo que querés |

---

## Interview Tips

- **Si te preguntan "¿qué hace TS distinto a Flow / a tipos de Java?"**, mencioná: structural typing, conditional types con `infer`, mapped types, control-flow narrowing. Estos cuatro juntos son únicos.
- **Si te muestran un error críptico de variancia**, dibujá el árbol `Crow <: Bird <: Animal` y razoná: parámetros se "abren" (contravariante), returns se "cierran" (covariante).
- **Si te piden tipear algo complejo (Redux store, ORM, API client)** y te trabás: separá en pasos — primero el shape básico, después mapped/conditional para derivar variantes.
- **El truco `const _: never = x` para exhaustividad** es una pregunta clásica de TS senior. Saber por qué funciona ya te diferencia.

---

## 📝 Ejercicios del libro

### Ej 1 — Asignabilidad

Decidir si el primer tipo es asignable al segundo:

| # | A | B | ¿A asignable a B? | Por qué |
|---|---|---|---|---|
| a | `1` | `number` | ✓ | `1` es subtipo de `number` (widened) |
| b | `number` | `1` | ✗ | un `number` cualquiera no es exactamente `1` |
| c | `string` | `number \| string` | ✓ | string ∈ union |
| d | `boolean` | `number` | ✗ | sin relación |
| e | `number[]` | `(number \| string)[]` | ✓ | arrays son covariantes en members |
| f | `(number\|string)[]` | `number[]` | ✗ | `string` no es number |
| g | `{ a: true }` | `{ a: boolean }` | ✓ | covariance: `true <: boolean` |
| h | `{ a: { b: [string] } }` | `{ a: { b: [number\|string] } }` | ✓ | covariance recursiva |
| i | `(a: number) => string` | `(b: number) => string` | ✓ | nombres de parámetros no importan |
| j | `(a: number) => string` | `(a: string) => string` | ✗ | param types: number no es supertipo de string |
| k | `(a: number\|string) => string` | `(a: string) => string` | ✓ | param: `number\|string >: string` (contravariante OK) |
| l | `E.X` (`enum E {X='X'}`) | `F.X` (`enum F {X='X'}`) | ✗ | enums son nominales |

### Ej 2 — keyof y keying-in

`type O = { a: { b: { c: string } } }`

- `keyof O` = `'a'`
- `O['a']['b']` = `{ c: string }`

### Ej 3 — `Exclusive<T, U>`

> "Tipos que están en T o U pero **no en ambos**" (XOR).

```typescript
type Exclusive<T, U> =
  | (T extends U ? never : T)
  | (U extends T ? never : U);

type R = Exclusive<1 | 2 | 3, 2 | 3 | 4>;  // 1 | 4
```

Evaluación paso a paso de `Exclusive<1 | 2, 2 | 4>`:

1. Lado izq: `(1 | 2) extends (2 | 4) ? never : (1 | 2)` — distribuye:
   - `1 extends (2|4) ? never : 1` = `1`
   - `2 extends (2|4) ? never : 2` = `never`
   - = `1 | never` = `1`
2. Lado der: `(2 | 4) extends (1 | 2) ? never : (2 | 4)` — distribuye:
   - `2 extends (1|2) ? never : 2` = `never`
   - `4 extends (1|2) ? never : 4` = `4`
   - = `4`
3. Unión: `1 | 4`. ✓

### Ej 4 — Reescribir el ejemplo de definite assignment sin `!`

En lugar de `let userId!: string`, fuerza el assign en una sola expresión:

```typescript
function fetchUser(): string {
  return globalCache.get('userId');
}

const userId = fetchUser();
userId.toUpperCase();  // ✓ — siempre asignado, sin bang
```

---

## 📚 References

- *Programming TypeScript* — Boris Cherny, O'Reilly 2019. Capítulo 6, "Advanced Types" (pp. 113–157).
- TypeScript Handbook — [Type Manipulation](https://www.typescriptlang.org/docs/handbook/2/types-from-types.html).
- Anders Hejlsberg, [Advanced Types](https://www.youtube.com/watch?v=hDACN-BGvI8) (TSConf).

---

> 📍 [⬅ Cap. 5: Classes & Interfaces](./05-classes-and-interfaces.md) · [Cap. 7: Handling Errors ➡](./07-handling-errors.md) · [📚 KB Index](../../../README.md)
