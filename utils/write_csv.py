import csv
def write_csv(results, output_file):
    with open(output_file, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Frame Number', 'License Plate Bbox (x1) (y1) (x2) (y2)', 'License Plate Text', 'License Plate Bbox Score', 'License Plate Text Score'])
        for frame_nmr, result in results.items():
            if 'license_plate' in result:
                bbox = result['license_plate']['bbox']
                text = result['license_plate']['text']
                bbox_score = result['license_plate']['bbox_score']
                text_score = result['license_plate']['text_score']
                writer.writerow([frame_nmr, bbox, text, bbox_score, text_score])