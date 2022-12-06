import java.nio.file.Files
import java.nio.file.Paths
import java.util.stream.Collectors

val input: String = Files.readString(Paths.get("inputs/day_6.txt"))

fun findSize(targetUnique: Int): Int = input.asSequence()
    .windowed(targetUnique)
    .takeWhile { it.toSet().size != targetUnique }
    .count() + targetUnique

println(findSize(4))
println(findSize(14))