import os

while True:
    os.system("clear")
    print("Доступные модели:")
    for file in os.listdir("./recipe/model"):
        parts = file.split(".")
        if len(parts) > 1 and parts[-1] == "joblib":
            print("\t" + file)
    
    data_ready = os.path.isfile("./input/data.scp") and os.path.isfile("./input/data.stm")
    vector_ready = os.path.isfile("./output/xvector.ark")

    print("\n" + "data.scp: " + ("ок" if data_ready else "не найден"))
    print("data.stm: " + ("ок" if data_ready else "не найден"))
    print("xvector.ark: " + ("ок" if vector_ready else "не найден"))
    print("\nДоступные действия:")
    print("\t1. Подготовить данные")
    if data_ready:
        print("\t2. Извлечь x-vector")
        if vector_ready:
            print("\t3. Обучить модель")
            print("\t4. Проверить модель")
    print("\t5. Выйти")
    cmd = input("Выберите действие -> ")
    if cmd == "5":
        os.system("clear")
        exit()
    if cmd == "1":
        answ = "y"
        if data_ready:
            print("Это действие перезапишет текущие data.scp и data.stm")
            answ = input("Продолжить? [y/n] -> ")
        if answ == "y" or answ == "Y":
            os.system("python3 ./prepare_data.py")
        input("Нажмите ENTER для продолжения...")
    elif data_ready:
        if cmd == "2":
            if vector_ready:
                print("Это действие перезапишет текущий xvector.ark")
                answ = input("Продолжить? [y/n] -> ")
                if answ == "y" or answ == "Y":
                    os.remove("./output/xvector.ark")
                else:
                    continue
            os.system("python3 ./recipe/local/xvector_utils.py make-xvectors ./input/data.scp ./input/data.stm ./output/xvector.ark")
            input("Нажмите ENTER для продолжения...")
        elif vector_ready:
            if cmd == "3":
                name = input("Введите имя новой модели (без .joblib) -> ")
                answ = "y"
                if os.path.isfile("./recipe/model/" + name + ".joblib"):
                    print("Текущее действие перезапишет модель " + name)
                    answ = input("Продолжить? [y/n] -> ")
                if answ == "y" or answ == "Y":
                    os.system("python3 ./recipe/local/xvector_utils.py train ./input/data.stm ./output/xvector.ark ./recipe/model/" + name + ".joblib")
                input("Нажмите ENTER для продолжения...")
            elif cmd == "4":
                name = input("Введите имя тестируемой модели (без .joblib) -> ")
                os.system("python3 ./recipe/local/xvector_utils.py evaluate ./input/data.stm ./output/xvector.ark ./recipe/model/" + name + ".joblib")
                input("Нажмите ENTER для продолжения...")
    
    continue
