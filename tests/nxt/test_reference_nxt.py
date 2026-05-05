from contexere.nxt import parse_args, reference_nxt

def test_no_references_specified():
    args = parse_args([''])
    assert [] == reference_nxt(args.reference, 'ERP26s5a')

def test_reference_requested():
    args = parse_args(['--reference'])
    assert ['ERP26s5a'] == reference_nxt(args.reference, 'ERP26s5a')

def test_one_reference_specified():
    args = parse_args(['--reference', 'ERP26s4a'])
    print(args)
    assert ['ERP26s4a'] == reference_nxt(args.reference, 'ERP26s5a')

def test_two_references_specified():
    args = parse_args(['--reference', 'ERP26s4a,b'])
    print(args)
    assert ['ERP26s4a', 'b'] == reference_nxt(args.reference, 'ERP26s5a')

    args = parse_args(['--reference', 'ERP26s4a,b', 'ERP26s5a'])
    print(args)
    assert ['ERP26s4a', 'b'] == reference_nxt(args.reference, 'ERP26s5a')

    args = parse_args(['ERP26s5a', '--reference', 'ERP26s4a,b'])
    print(args)
    assert ['ERP26s4a', 'b'] == reference_nxt(args.reference, 'ERP26s5a')

