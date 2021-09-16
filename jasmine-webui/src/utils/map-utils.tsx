export function arrayFromMap<KeyType, ValueType, ElemType>(
    values: Map<KeyType, ValueType>,
    mapperFunc: (key: KeyType, value: ValueType) => ElemType
): ElemType[] {
    return Array.from(values.entries()).map(([key, value]) =>
        mapperFunc(key, value)
    );
}

export function mapFromArray<ElemType, KeyType, ValueType>(
    values: ElemType[],
    mapperFunc: (elem: ElemType) => [KeyType, ValueType]
): Map<KeyType, ValueType> {
    return new Map(values.map(mapperFunc));
}

export function mapApply<KeyType, ValueType, NewKeyType, NewValueType>(
    values: Map<KeyType, ValueType>,
    mapperFunc: (key: KeyType, value: ValueType) => [NewKeyType, NewValueType]
): Map<NewKeyType, NewValueType> {
    const result = new Map<NewKeyType, NewValueType>();
    for (const [key, value] of values.entries()) {
        const [newKey, newValue] = mapperFunc(key, value);
        console.assert(!result.has(newKey), "Duplicate key " + newKey + ".");
        result.set(newKey, newValue);
    }
    return result;
}

export function groupedItems(
    values: Map<string, any>,
    groupKeyFunc: (key: string) => string
): Map<string, Map<string, any>> {
    let result = new Map();

    for (const [key, value] of values.entries()) {
        const groupKey = groupKeyFunc(key) as string;

        if (!result.has(groupKey)) {
            result.set(groupKey, new Map());
        }
        result.get(groupKey).set(key, value);
    }

    return result;
}

export function withoutKeyPrefix<ValueType>(
    values: Map<string, ValueType>
): Map<string, ValueType> {
    return mapApply(values, (key, value) => [
        key.split("/").slice(1).join("/"),
        value,
    ]);
}

export type RecursiveMap<ValueType> =
    | ValueType
    | Map<string, RecursiveMap<ValueType>>;

export function unflattenedMap<ValueType>(
    values: Map<string, ValueType>
): RecursiveMap<ValueType> {
    let subdirItemGroups = groupedItems(values, (key: any) => {
        const [first] = key.split("/");
        return first;
    });

    return mapApply(subdirItemGroups, (subdir, subdirItems) => {
        subdirItems = withoutKeyPrefix(subdirItems);

        if (subdirItems.has("")) return [subdir, subdirItems.get("")];
        else return [subdir, unflattenedMap(subdirItems)];
    });
}
