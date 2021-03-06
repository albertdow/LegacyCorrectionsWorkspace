/*****************************************************************************
 * Project: RooFit                                                           *
 *                                                                           *
 * This code was autogenerated by RooClassFactory                            *
 *****************************************************************************/

#ifndef CRYSTALBALLEFFICIENCY
#define CRYSTALBALLEFFICIENCY

#include "RooAbsCategory.h"
#include "RooAbsReal.h"
#include "RooAbsReal.h"
#include "RooCategoryProxy.h"
#include "RooRealProxy.h"

class CrystalBallEfficiency : public RooAbsReal {
 public:
  CrystalBallEfficiency(){};
  CrystalBallEfficiency(const char* name, const char* title, RooAbsReal& _m,
                        RooAbsReal& _m0, RooAbsReal& _sigma, RooAbsReal& _alpha,
                        RooAbsReal& _n, RooAbsReal& _norm);
  CrystalBallEfficiency(const CrystalBallEfficiency& other,
                        const char* name = 0);
  virtual TObject* clone(const char* newname) const {
    return new CrystalBallEfficiency(*this, newname);
  }
  inline virtual ~CrystalBallEfficiency() {}

 protected:
  RooRealProxy m;
  RooRealProxy m0;
  RooRealProxy sigma;
  RooRealProxy alpha;
  RooRealProxy n;
  RooRealProxy norm;

  Double_t evaluate() const;

 private:
  ClassDef(CrystalBallEfficiency, 1)
};

#endif
