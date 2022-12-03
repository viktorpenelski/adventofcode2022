import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.util.stream.Collectors

val input: List<String> = Files.lines(Paths.get("inputs/day_3.txt")).collect(Collectors.toList())

fun calculatePriority(char: Char): Int {
    //println("char: $char toInt: ${char.toInt()}")
    if (char.toInt() >= 'a'.toInt() && char.toInt() <= 'z'.toInt()) {
        return 1 + char.toInt() - 'a'.toInt()
    }
    return 27 + char.toInt() - 'A'.toInt()
}

fun commonItemFrom(bags: List<String>): Char {
    return bags.map { it.toSet() }
        .reduce { acc, bag -> bag.intersect(acc) }
        .first()
}

val partOne = input.map { commonItemFrom(it.chunked(it.length / 2)) }
    .sumBy { calculatePriority(it) }

println(partOne)

val partTwo = input.windowed(size = 3, step = 3)
    .map { commonItemFrom(it) }
    .sumBy { calculatePriority(it) }

println(partTwo)
