// Filename: cImpulse.cxx
// Created by:  darren (13Jul04)
//
////////////////////////////////////////////////////////////////////

#include "cImpulse.h"
#include "cMover.h"

TypeHandle CImpulse::_type_handle;

////////////////////////////////////////////////////////////////////
//     Function: CImpulse::Constructor
//       Access: Public
//  Description:
////////////////////////////////////////////////////////////////////
CImpulse::
CImpulse() :
  _mover(0)
{
}

////////////////////////////////////////////////////////////////////
//     Function: CImpulse::Destructor
//       Access: Public, Virtual
//  Description:
////////////////////////////////////////////////////////////////////
CImpulse::
~CImpulse() {
  nassertv(_mover == 0);
}

////////////////////////////////////////////////////////////////////
//     Function: CImpulse::process
//       Access: Public, Virtual
//  Description: override this and set your impulse's influence for
//               this pass on its mover
////////////////////////////////////////////////////////////////////
void CImpulse::
process(float dt) {
}

////////////////////////////////////////////////////////////////////
//     Function: CImpulse::set_mover
//       Access: Public, Virtual
//  Description: called internally by cMover when we're added
////////////////////////////////////////////////////////////////////
void CImpulse::
set_mover(CMover &mover) {
  _mover = &mover;
  _node_path = _mover->get_node_path();
}

////////////////////////////////////////////////////////////////////
//     Function: CImpulse::clear_mover
//       Access: Public, Virtual
//  Description: called internally by cMover when we're removed
////////////////////////////////////////////////////////////////////
void CImpulse::
clear_mover(CMover &mover) {
  if (_mover == &mover) {
    _mover = 0;
    _node_path.clear();
  } else {
    cerr << "clear_mover: unknown CMover" << std::endl;
  }
}