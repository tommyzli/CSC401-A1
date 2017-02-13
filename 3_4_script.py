import subprocess
import sys
from scipy import stats


tweets_per_polarity_per_file = 20000 / 10 / 2


class AllDoneException(Exception):
    pass


def find_available_file_with_polarity(polarity, output_dict):
    for key, val in output_dict.iteritems():
        total = val[polarity]
        if total < tweets_per_polarity_per_file:
            return key

    # every output is full
    raise AllDoneException()

if __name__ == '__main__':
    # Training file path
    input_path = sys.argv[1]

    print "creating individual and concatenated partitions"

    # Partition training file
    outputs = {
        index: {
            'file': open('partition_{}.arff'.format(index), 'w'),
            '0': 0,
            '4': 0,
        }
        for index in range(1, 11)
    }
    for key, val in outputs.iteritems():
        output_file = val['file']

    with open(input_path, 'r') as training_file:
        for line in training_file:
            if not line[0].isdigit():
                continue
            polarity = line[-2]
            try:
                key_to_write = find_available_file_with_polarity(polarity, outputs)
            except AllDoneException:
                break
            outputs[key_to_write]['file'].write(line)
            outputs[key_to_write][polarity] += 1

    for output_file in outputs.itervalues():
        output_file['file'].close()  # Combine partitions

    # exclude_x.arff is a concatenation of all partitions except for partition_x.arff
    outputs = {
        index: open('exclude_{}.arff'.format(index), 'w')
        for index in range(1, 11)
    }
    inputs = {
        index: open('partition_{}.arff'.format(index), 'r')
        for index in range(1, 11)
    }

    # content of each partition, stored separately from the file pointer so the file can be closed later
    input_lines = {
        index: f.readlines()
        for index, f in inputs.iteritems()
    }

    for output_index, output_file in outputs.iteritems():
        output_file.write('@RELATION exclude_{}.arff\n\n'.format(output_index))
        output_file.write('@ATTRIBUTE first_person_pronouns NUMERIC\n')
        output_file.write('@ATTRIBUTE second_person_pronouns NUMERIC\n')
        output_file.write('@ATTRIBUTE third_person_pronouns NUMERIC\n')
        output_file.write('@ATTRIBUTE coordinating_conjunctions NUMERIC\n')
        output_file.write('@ATTRIBUTE past_tense_verbs NUMERIC\n')
        output_file.write('@ATTRIBUTE future_tense_verbs NUMERIC\n')
        output_file.write('@ATTRIBUTE commas NUMERIC\n')
        output_file.write('@ATTRIBUTE colons_and_semicolons NUMERIC\n')
        output_file.write('@ATTRIBUTE dashes NUMERIC\n')
        output_file.write('@ATTRIBUTE parentheses NUMERIC\n')
        output_file.write('@ATTRIBUTE ellipses NUMERIC\n')
        output_file.write('@ATTRIBUTE common_nouns  NUMERIC\n')
        output_file.write('@ATTRIBUTE proper_nouns NUMERIC\n')
        output_file.write('@ATTRIBUTE adverbs NUMERIC\n')
        output_file.write('@ATTRIBUTE wh_words NUMERIC\n')
        output_file.write('@ATTRIBUTE slang_acronyms NUMERIC\n')
        output_file.write('@ATTRIBUTE uppercase_words NUMERIC\n')
        output_file.write('@ATTRIBUTE average_length_of_sentences NUMERIC\n')
        output_file.write('@ATTRIBUTE average_length_of_tokens NUMERIC\n')
        output_file.write('@ATTRIBUTE number_of_sentences NUMERIC\n')
        output_file.write('@ATTRIBUTE polarity {0, 4}\n\n')
        output_file.write('@DATA\n')

        indexes_to_include = range(1, 11)
        indexes_to_include.remove(output_index)
        for partition_index in indexes_to_include:
            output_file.writelines(
                input_lines[partition_index]
            )

    for i in range(1, 11):
        outputs[i].close()
        inputs[i].close()

    # Add ARFF headers into each partition file
    for index in range(1, 11):
        with open('partition_{}.arff'.format(index), 'w') as new_partition:
            new_partition.write('@RELATION partition_{}.arff\n\n'.format(index))
            new_partition.write('@ATTRIBUTE first_person_pronouns NUMERIC\n')
            new_partition.write('@ATTRIBUTE second_person_pronouns NUMERIC\n')
            new_partition.write('@ATTRIBUTE third_person_pronouns NUMERIC\n')
            new_partition.write('@ATTRIBUTE coordinating_conjunctions NUMERIC\n')
            new_partition.write('@ATTRIBUTE past_tense_verbs NUMERIC\n')
            new_partition.write('@ATTRIBUTE future_tense_verbs NUMERIC\n')
            new_partition.write('@ATTRIBUTE commas NUMERIC\n')
            new_partition.write('@ATTRIBUTE colons_and_semicolons NUMERIC\n')
            new_partition.write('@ATTRIBUTE dashes NUMERIC\n')
            new_partition.write('@ATTRIBUTE parentheses NUMERIC\n')
            new_partition.write('@ATTRIBUTE ellipses NUMERIC\n')
            new_partition.write('@ATTRIBUTE common_nouns  NUMERIC\n')
            new_partition.write('@ATTRIBUTE proper_nouns NUMERIC\n')
            new_partition.write('@ATTRIBUTE adverbs NUMERIC\n')
            new_partition.write('@ATTRIBUTE wh_words NUMERIC\n')
            new_partition.write('@ATTRIBUTE slang_acronyms NUMERIC\n')
            new_partition.write('@ATTRIBUTE uppercase_words NUMERIC\n')
            new_partition.write('@ATTRIBUTE average_length_of_sentences NUMERIC\n')
            new_partition.write('@ATTRIBUTE average_length_of_tokens NUMERIC\n')
            new_partition.write('@ATTRIBUTE number_of_sentences NUMERIC\n')
            new_partition.write('@ATTRIBUTE polarity {0, 4}\n\n')
            new_partition.write('@DATA\n')
            new_partition.writelines(input_lines[index])

    # Run WEKA classifications
    print "Running cross validation, this will take some time"
    weka_classifiers = {
        'cross_val_bayes': 'weka.classifiers.bayes.NaiveBayes',
        'cross_val_j48': 'weka.classifiers.trees.J48',
        'cross_val_smo': 'weka.classifiers.functions.SMO',
    }
    cross_val_files = ['cross_val_bayes', 'cross_val_j48', 'cross_val_smo']
    for filename in cross_val_files:
        with open(filename, 'w') as output_file:
            for i in range(1, 11):
                subprocess.call(
                    'java -cp /u/cs401/WEKA/weka.jar {0} -o -t exclude_{1}.arff -T partition_{2}.arff'.format(weka_classifiers[filename], i, i),
                    shell=True,
                    stdout=output_file
                )

    accuracies = {filename: [] for filename in cross_val_files}
    print "Partition\tAccuracy\tPrecision(a)\tPrecision(b)\tRecall(a)\tRecall(b)"
    for filename in cross_val_files:
        # strip all classification data except for testing data confusion matrices
        with open(filename, 'r') as classification_output:
            lines = classification_output.readlines()
            # keep only lines that start with a number (this strips everything except the confusion matrices)
            lines_to_keep = [
                line
                for line in lines
                if len(line.lstrip()) > 0 and line.lstrip()[0].isdigit()
            ]

        index = 0
        testing_matrix_lines = []
        for i, j in zip(lines_to_keep[0::2], lines_to_keep[1::2]):  # Go through the list two items at a time
            # keep every other set of two lines, as they alternate between two lines for training matrix, two lines for testing matrix
            if index % 2 != 0:
                testing_matrix_lines.append(i)
                testing_matrix_lines.append(j)
            index = index + 1

        print "Calculating accuracy, precision and recall for {}".format(filename)
        current_matrix = {}
        i = 1
        for index, line in enumerate(testing_matrix_lines):
            even = index % 2 == 0
            values = line.rstrip().lstrip().split()
            values = [int(val) for val in values if val.isdigit()]

            if even:
                current_matrix[0] = values
            else:
                current_matrix[1] = values

            if not even:
                # print i
                total = current_matrix[0][0] + current_matrix[0][1] + current_matrix[1][0] + current_matrix[1][1]
                accuracy = (current_matrix[0][0] + current_matrix[1][1]) / float(total)
                # print "accuracy: {}".format(accuracy)
                accuracies[filename].append(accuracy)

                precisiona = current_matrix[0][0] / float(current_matrix[0][0] + current_matrix[0][1])
                # print "precision a: {}".format(precisiona)

                precisionb = current_matrix[1][1] / float(current_matrix[1][0] + current_matrix[1][1])
                # print "precision b: {}".format(precisionb)

                recalla = current_matrix[0][0] / float(current_matrix[0][0] + current_matrix[1][0])
                # print "recall a: {}".format(recalla)

                recallb = current_matrix[1][1] / float(current_matrix[1][1] + current_matrix[0][1])
                # print "recall b: {}".format(recallb)
                print "{0}\t{1}\t{2}\t{3}\t{4}".format(
                    i,
                    accuracy,
                    precisiona,
                    precisionb,
                    recalla,
                    recallb,
                )
                i = i + 1
                current_matrix = {}

    print ""
    print "P-values:"
    pval = stats.ttest_rel(accuracies['cross_val_bayes'], accuracies['cross_val_smo']).pvalue
    print "Bayes and SMO: {}".format(pval)

    pval = stats.ttest_rel(accuracies['cross_val_smo'], accuracies['cross_val_j48']).pvalue
    print "SMO and J48: {}".format(pval)

    pval = stats.ttest_rel(accuracies['cross_val_bayes'], accuracies['cross_val_j48']).pvalue
    print "Bayes and J48: {}".format(pval)
